# storyboard.json 형식

```json
{
  "output": "shorts/demo/short.mp4",
  "voiceover": "shorts/demo/vo.mp3",
  "music": "shorts/demo/bgm.mp3",
  "music_volume": 0.15,
  "font": "Noto Sans CJK KR",
  "scenes": [
    {"duration": 3, "caption": "첫 줄\n둘째 줄", "media": "shorts/demo/a.jpg"},
    {"duration": 2.5, "media": "shorts/demo/b.mp4",
     "captions": [{"text": "앞부분", "start": 0, "end": 1.2}, {"text": "뒷부분", "start": 1.2, "end": 2.5}]},
    {"duration": 3, "caption": "저장해두세요", "background": "#1c1c28", "note": "소재 미정 → 단색 카드"}
  ]
}
```

| 필드 | 필수 | 설명 |
|---|---|---|
| `output` | 아니오 | 결과 mp4 경로 (기본 `short.mp4`). 폴더는 자동 생성 |
| `voiceover` | 아니오 | 내레이션 오디오(mp3/wav/m4a). 장면 길이 합보다 길면 잘림 |
| `music` | 아니오 | 배경음. 길이가 모자라면 반복. 내레이션이 있으면 기본 볼륨 0.15 |
| `music_volume` | 아니오 | 0~1 |
| `font` | 아니오 | 자막 폰트 패밀리. 비우면 한글 지원 폰트를 자동 탐색 |
| `scenes[].duration` | 예 | 초 단위. 권장 1.5~4초 |
| `scenes[].media` | 아니오 | 이미지(jpg/png/webp)는 천천히 확대되는 효과, 영상은 중앙 크롭 후 길이에 맞게 잘리거나 반복. 없으면 단색 배경 |
| `scenes[].caption` | 아니오 | 장면 내내 표시. `\n`으로 줄바꿈 |
| `scenes[].captions` | 아니오 | 장면 안에서 나눠 표시할 때 `{text,start,end}` 목록 (장면 시작 기준 초) |
| `scenes[].background` | 아니오 | 미디어 없을 때 배경색 `#RRGGBB` |
| `scenes[].note` | 아니오 | 사람용 메모. 렌더에 영향 없음 |

## 동작 메모

- 출력은 1080x1920, 30fps, H.264 + AAC, `+faststart`.
- 자막은 하단에서 520px 위(`--caption-margin`)에 놓인다. 릴스/쇼츠의 하단 UI(계정명·캡션·버튼)에 가리지 않기 위함. 실제 업로드 전 미리보기로 한 번 확인한다.
- 미디어 경로는 스크립트를 실행하는 위치 기준이다.
- 장면별 클립을 먼저 만들어 이어붙이므로 장면 수가 많아도 메모리 부담이 적다.
