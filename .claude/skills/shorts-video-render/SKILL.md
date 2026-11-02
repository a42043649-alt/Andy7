---
name: shorts-video-render
description: 스토리보드(storyboard.json)와 이미지·영상·내레이션·음악 파일로 1080x1920 세로 숏폼 mp4(릴스/쇼츠/틱톡용)를 ffmpeg로 실제 렌더링한다. 한글 자막 번인, 이미지 줌 효과, 영상 크롭, 음악 믹스 포함. 사용자가 "영상 만들어줘", "렌더해줘", "mp4로 뽑아줘", "자막 입혀줘", "이미지로 쇼츠 만들기", "세로 영상 합성"을 말하면 반드시 사용한다.
compatibility: ffmpeg(libass 포함), ffprobe, python3 필요. 한글 폰트(Noto Sans CJK KR / Pretendard / 나눔고딕 등) 권장.
---

# 숏폼 렌더

`scripts/render_short.py`가 storyboard.json을 읽어 장면별 클립을 만들고, 이어붙이고, 자막과 오디오를 얹어 최종 mp4를 만든다. 직접 ffmpeg 명령을 매번 짜지 말고 이 스크립트를 쓴다 — 세로 크롭, 자막 안전영역, 한글 폰트 탐색 같은 함정을 이미 처리해뒀다.

## 절차

1. `storyboard.json`이 없으면 `shorts-storyboard` 스킬로 먼저 만든다. 형식은 `references/storyboard-spec.md`.
2. 소재 파일 경로가 모두 맞는지, 내레이션이 있으면 길이와 장면 합이 맞는지 확인한다:
   ```bash
   python .claude/skills/shorts-video-render/scripts/render_short.py storyboard.json --dry-run
   ```
3. 렌더:
   ```bash
   python .claude/skills/shorts-video-render/scripts/render_short.py storyboard.json
   ```
   옵션: `--font "폰트명"`, `--font-size 68`, `--caption-margin 520`.
4. 결과 확인: 길이·해상도를 `ffprobe`로 확인하고, 가능하면 중간 프레임을 한 장 뽑아 자막 위치와 글자 깨짐을 눈으로 본다:
   ```bash
   ffmpeg -y -ss 1 -i short.mp4 -frames:v 1 check.png
   ```
5. 사용자에게 출력 경로, 길이, 경고 사항(소재 없는 장면, 길이 초과 등)을 알려준다.

## 자주 생기는 문제

- **한글이 네모(□)로 나옴**: 한글 폰트가 없다. `fc-list :lang=ko`로 확인하고 `--font`로 지정하거나 폰트를 설치한다.
- **영상이 늘어나거나 여백이 생김**: 스크립트가 중앙 크롭으로 채우므로 정상이다. 피사체가 잘리면 원본을 세로 구도로 다시 찍거나 장면을 바꾼다.
- **내레이션이 잘림**: 장면 `duration` 합을 내레이션 길이 이상으로 늘린다.
- **60초 초과 경고**: 쇼츠로 분류되는 길이 한도에 걸릴 수 있다. 장면을 줄인다.

## 범위

이 스크립트는 합성·자막·믹스만 한다. 소재 생성(AI 이미지, TTS, 음원 다운로드)은 하지 않는다 — 사용자가 가진 도구로 만든 파일을 받아 쓴다. 전환 효과나 정교한 컷 편집이 필요하면 스크립트를 확장하기보다 편집 앱을 권한다.
