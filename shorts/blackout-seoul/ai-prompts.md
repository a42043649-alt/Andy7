# Higgsfield 생성 프롬프트 — "만약 서울이 3일간 정전된다면?"

각 컷을 **9:16 세로**로 생성하세요. 아래 프롬프트 뒤에 **공통 접미사**를 붙이면 둥글고 사실적인 톤이 일관됩니다.
생성·다운로드한 파일을 `shorts/blackout-seoul/src/`에 표의 "저장 파일명"으로 넣고 알려주시면, 제가 자막·음악·훅을 얹어 완성합니다.

**공통 접미사 (프롬프트 끝에 붙이기):**
```
photorealistic, cinematic, realistic proportions, soft rounded natural forms, volumetric lighting,
natural textures, shot on film, highly detailed, slow continuous camera move,
NOT low-poly, NOT blocky, NOT angular, no HUD, no on-screen text, no subtitles
```

**추천 설정**: 종횡비 `9:16`, 길이 컷당 `5초`, 오디오(generate_audio)는 **끄기**(off) — 음악은 제가 따로 얹습니다. 무료 크레딧 10개로는 2~3컷만 가능하니, 먼저 1·2·4번(가장 임팩트 큰 컷)부터 뽑아보길 권합니다.

| # | 프롬프트 (영어 권장, 뒤에 공통 접미사) | 추천 모델 | 저장 파일명 |
|---|---|---|---|
| 1 | Aerial drone shot slowly descending over Seoul skyline at dusk, city lights just flickering on, warm heat haze over Han river, orange sky | Cinema Studio 3.0 또는 Seedance 2.0 | `01_dusk.mp4` |
| 2 | An electrical substation overloads with soft sparks, then a Gangnam street's lights and neon signs cut to black one by one, evening | MiniMax Hailuo (물리/스파크) | `02_blackout.mp4` |
| 3 | A busy intersection as traffic lights die and cars slow in confusion; cut to a subway train stopped still inside a dark tunnel, emergency lighting | MiniMax Hailuo 또는 Seedance 2.0 | `03_stop.mp4` |
| 4 | High aerial view of Seoul at night as a wave of darkness spreads district by district, blocks of lights going out across the city | Cinema Studio 3.0 | `04_darkwave.mp4` |
| 5 | Street level at night, people gathered with flashlights and candles outside a convenience store lit by a single emergency lamp, calm faces | Seedance 2.0 (인물 일관성) | `05_people.mp4` |
| 6 | A fully dark Seoul cityscape under a sky suddenly full of stars and a faint Milky Way, silhouettes of apartment towers, serene and eerie | Cinema Studio 3.0 | `06_stars.mp4` |
| 7 | Pre-dawn Seoul as electric light cascades back on across the city, windows and streetlights glowing to life block by block, hopeful | Seedance 2.0 또는 Cinema Studio 3.0 | `07_restore.mp4` |

## 팁
- **"한 샷 추적" 느낌**이 이 스타일의 핵심입니다. 프롬프트에 "slow continuous camera"를 꼭 남기세요.
- 사람 얼굴이 어색하면 인물 컷(3·5번)은 **Seedance 2.0**이 가장 안정적입니다.
- 각진 느낌이 나오면 프롬프트에 `rounded, realistic, NOT low-poly`를 더 강조하거나 cfg/genre를 조정하세요.
- 컷이 5초인데 대본은 4~5초라 거의 맞습니다. 좀 길면 제가 렌더 시 잘라서 맞춥니다.
