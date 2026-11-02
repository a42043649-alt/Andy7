#!/usr/bin/env python3
"""Render a 1080x1920 short-form video from a storyboard JSON using ffmpeg.

Usage:
    python render_short.py storyboard.json [--font "Noto Sans CJK KR"] [--dry-run]

See references/storyboard-spec.md for the JSON format.
Paths inside the JSON are resolved relative to the current working directory.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

W, H, FPS = 1080, 1920, 30
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}
FONT_FALLBACKS = ["Noto Sans CJK KR", "Pretendard", "NanumGothic", "Malgun Gothic",
                  "Apple SD Gothic Neo", "WenQuanYi Zen Hei"]


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        tail = "\n".join(p.stderr.strip().splitlines()[-12:])
        die(f"ffmpeg failed:\n  {' '.join(map(str, cmd))}\n{tail}")


def pick_font(requested):
    """Return a font family that fontconfig can actually find (Hangul needs a CJK font)."""
    candidates = ([requested] if requested else []) + FONT_FALLBACKS
    if not shutil.which("fc-list"):
        return candidates[0]
    for name in candidates:
        out = subprocess.run(["fc-list", name], capture_output=True, text=True).stdout
        if out.strip():
            return name
    print("warning: no Korean-capable font found; Hangul captions may render as boxes",
          file=sys.stderr)
    return candidates[0]


def ass_time(t):
    cs = int(round(t * 100))
    h, rem = divmod(cs, 360000)
    m, rem = divmod(rem, 6000)
    s, cs = divmod(rem, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def ass_escape(text):
    return text.replace("\\", "").replace("{", "(").replace("}", ")").replace("\n", "\\N")


def build_ass(scenes, font, size, margin_v):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,2,2,90,90,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines, t = [], 0.0
    for sc in scenes:
        d = sc["duration"]
        items = sc.get("captions")
        if not items and sc.get("caption"):
            items = [{"text": sc["caption"], "start": 0, "end": d}]
        for it in items or []:
            s = t + float(it.get("start", 0))
            e = t + min(float(it.get("end", d)), d)
            lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Default,,0,0,0,,{ass_escape(it['text'])}")
        t += d
    return head + "\n".join(lines) + "\n"


def scene_filter_image(d):
    frames = max(1, int(round(d * FPS)))
    # Slow zoom-in (Ken Burns). Upscale first so the zoom stays smooth.
    return (f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
            f"zoompan=z='min(zoom+0.0006,1.12)':d={frames}:"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},setsar=1,format=yuv420p")


def render_scene(sc, idx, tmp):
    d = sc["duration"]
    out = tmp / f"scene_{idx:03d}.mp4"
    media = sc.get("media")
    common = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
              "-r", str(FPS), "-an", "-t", str(d), str(out)]
    if media:
        p = Path(media)
        if not p.exists():
            die(f"scene {idx+1}: media not found: {media}")
        ext = p.suffix.lower()
        if ext in IMAGE_EXT:
            cmd = ["ffmpeg", "-y", "-i", str(p), "-vf", scene_filter_image(d)] + common
        elif ext in VIDEO_EXT:
            vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                  f"fps={FPS},setsar=1,format=yuv420p")
            cmd = ["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(p), "-vf", vf] + common
        else:
            die(f"scene {idx+1}: unsupported media type: {media}")
    else:
        color = sc.get("background", "#1c1c28").lstrip("#")
        cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=0x{color}:s={W}x{H}:r={FPS}"] + common
    run(cmd)
    return out


def probe_duration(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(p.stdout.strip())
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--font", help="caption font family (default: auto-detect a Korean font)")
    ap.add_argument("--font-size", type=int, default=68)
    ap.add_argument("--caption-margin", type=int, default=520,
                    help="px from bottom to caption baseline; keeps text above platform UI")
    ap.add_argument("--dry-run", action="store_true", help="validate and print the plan only")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            die(f"{tool} not found. Install ffmpeg first.")

    spec = json.loads(Path(args.storyboard).read_text(encoding="utf-8"))
    scenes = spec.get("scenes") or die("storyboard has no scenes")
    for i, sc in enumerate(scenes):
        if not isinstance(sc.get("duration"), (int, float)) or sc["duration"] <= 0:
            die(f"scene {i+1}: 'duration' (seconds, > 0) is required")
    total = sum(sc["duration"] for sc in scenes)
    output = Path(spec.get("output", "short.mp4"))

    vo, music = spec.get("voiceover"), spec.get("music")
    for label, f in (("voiceover", vo), ("music", music)):
        if f and not Path(f).exists():
            die(f"{label} file not found: {f}")
    if vo:
        vd = probe_duration(vo)
        if vd and vd > total + 0.3:
            print(f"warning: voiceover ({vd:.1f}s) is longer than scenes ({total:.1f}s); it will be cut",
                  file=sys.stderr)

    print(f"{len(scenes)} scenes, {total:.1f}s total -> {output}")
    if total > 60:
        print("warning: over 60s; some platforms/formats will not treat this as a Short",
              file=sys.stderr)
    missing = [i + 1 for i, s in enumerate(scenes) if not s.get("media")]
    if missing:
        print(f"note: scenes {missing} have no media; using solid background cards")
    if args.dry_run:
        return

    font = pick_font(args.font or spec.get("font"))
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="shorts_") as t:
        tmp = Path(t)
        clips = [render_scene(sc, i, tmp) for i, sc in enumerate(scenes)]
        (tmp / "list.txt").write_text("".join(f"file '{c.name}'\n" for c in clips))
        (tmp / "subs.ass").write_text(
            build_ass(scenes, font, args.font_size, args.caption_margin), encoding="utf-8")

        inputs = ["-f", "concat", "-safe", "0", "-i", "list.txt"]
        fc, amap, n = [], [], 1
        if vo:
            inputs += ["-i", str(Path(vo).resolve())]
            fc.append(f"[{n}:a]volume=1.0[vo]"); amap.append("[vo]"); n += 1
        if music:
            inputs += ["-stream_loop", "-1", "-i", str(Path(music).resolve())]
            vol = spec.get("music_volume", 0.15 if vo else 0.8)
            fc.append(f"[{n}:a]volume={vol}[bg]"); amap.append("[bg]"); n += 1
        if len(amap) == 2:
            fc.append("[vo][bg]amix=inputs=2:duration=longest:normalize=0[a]")
            audio_label = "[a]"
        elif amap:
            audio_label = amap[0]
        else:
            audio_label = None

        fc.insert(0, "[0:v]ass=subs.ass[v]")
        cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", ";".join(fc), "-map", "[v]"]
        if audio_label:
            cmd += ["-map", audio_label, "-c:a", "aac", "-b:a", "192k"]
        cmd += ["-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                str(output.resolve())]
        run(cmd, cwd=tmp)

    print(f"done: {output}  (font: {font})")


if __name__ == "__main__":
    main()
