# "달에서 인류가 산다면?" — 장면별 AI 생성 프롬프트

각 장면마다 **이미지용**(Midjourney·Nano Banana·DALL·E 등 → 렌더 시 자동 줌)과
**영상용**(Veo·Sora·Runway·Kling 등 → 바로 움직이는 클립) 프롬프트를 둘 다 넣었다.
둘 중 편한 도구로 만들어 `shorts/moon-life/`에 저장하고, `storyboard.json`의 각 장면
`media` 값을 그 파일 경로로 바꾼 뒤 다시 렌더하면 완성된다.

**공통 스타일 접미사** (프롬프트 끝에 붙이면 톤이 일관됨):
`cinematic, photorealistic, vertical 9:16, dramatic lighting, shot on 35mm, highly detailed, no text`

| # | 자막 | 이미지/영상 프롬프트 (영어 권장) | 저장 파일 |
|---|---|---|---|
| 1 | 달에서 살면 벌어지는 6가지 | A vast futuristic lunar colony with glass domes on the gray moon surface, planet Earth hanging huge in the pitch-black starry sky, wide establishing shot | scene1.jpg / .mp4 |
| 2 | ① 하루가 지구의 한 달 | The sun grazing slowly along the lunar horizon casting extremely long shadows across craters, subtle time-lapse motion | scene2.jpg / .mp4 |
| 3 | ② 몸무게가 6분의 1로 | An astronaut in a sleek white future spacesuit performing a slow high floating jump in low gravity, dust rising softly | scene3.jpg / .mp4 |
| 4 | ③ 집은 땅속 용암동굴에 | Interior of a lunar lava tube cave converted into cozy habitation modules, warm glowing lights, people living inside | scene4.jpg / .mp4 |
| 5 | ④ 물은 달 남극 얼음에서 | A robotic rover mining bright water ice inside a dark permanently-shadowed polar crater, headlights cutting the darkness | scene5.jpg / .mp4 |
| 6 | ⑤ 창밖엔 거대한 지구가 | POV through a large dome window of an 'Earthrise', the blue planet rising over gray lunar regolith, serene | scene6.jpg / .mp4 |
| 7 | ⑥ 가족과 통화엔 1.3초의 틈 | A lonely colonist making a glitchy blue holographic video call to family inside a dim cozy moon habitat | scene7.jpg / .mp4 |
| 8 | 당신이라면, 달에 살래요? | Back view silhouette of a single person standing on the lunar surface looking up at the distant Earth, emotional, wide | scene8.jpg / .mp4 |

## 교체 방법 (예시)

`storyboard.json`에서:
```json
{"duration": 3.5, "caption": "달에서 살면\n벌어지는 6가지", "media": "shorts/moon-life/scene1.jpg"}
```
처럼 `media`를 바꾸고 저장소 루트에서:
```bash
python3 .claude/skills/shorts-video-render/scripts/render_short.py shorts/moon-life/storyboard.json
```

## 내레이션(선택)

대본 표의 내레이션을 TTS로 만들어 `vo.mp3`로 저장하고 `storyboard.json`의
`"voiceover": "shorts/moon-life/vo.mp3"`로 지정하면 목소리가 깔린다.
배경음악 파일이 있으면 `"music": "..."`도 지정 (내레이션과 함께 쓰면 자동으로 작게 믹스).

## 어떤 AI 도구?

- **영상 직접 생성(가장 그럴듯함):** Google Veo, OpenAI Sora, Runway Gen-3, Kling, Luma — 텍스트→동영상
- **이미지 생성 후 줌:** Midjourney, Google Flow(Nano Banana), DALL·E, Stable Diffusion — 렌더 스크립트가 천천히 확대해 줌
- 상업 업로드면 생성물의 상업적 사용 가능 여부를 각 도구 약관에서 확인할 것.
