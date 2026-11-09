---
name: bf-caption
description: 대나무숲 게시물·대숲툰 캡션을 계정 형식대로 쓰고 caption_check.py 로 점검한다. "캡션 써줘", "캡션 고쳐줘", "해시태그", posts/NNN/post.json 의 caption 작성·수정 요청에 사용.
---

# bf-caption — 캡션

대숲툰 캡션은 `tools/toon/render.py` 의 `caption()` 이 원고에서 자동으로 만든다. 이 스킬은 **원고 값(hook·tips·sum·question·next·tags)을 다듬거나**, 일반 게시물(posts/NNN) 캡션을 직접 쓸 때 쓴다.

## 형식 (존댓말, 계정 말투)
1. 첫 줄: 후킹 + 🎋 (`/bf-hook`)
2. "대숲툰 N화 · 부제"
3. ✔ 팁 3개 (각 10자 안팎)
4. "오늘의 한 줄 ▶ …" 위로가 되는 한 문장
5. 댓글 유도 질문 하나 + 👇
6. "다음 화 ▶ …"
7. 💌 사연 접수 안내 (익명 보장)
8. 해시태그 8~12개, `#대나무숲` 필수, 화별 태그 2개

## 점검
```
python3 caption_check.py posts/NNN/post.json
```
`ERROR` 는 반드시 고친다 (보험료·보험금·청구·고지의무·세액공제·수수료·상품명·보험사명·가입 권유). `WARN` 은 이유가 있으면 둬도 된다.

## 하지 말 것
- 훈계, 실적 압박, 고객 탓
- 실제 오픈채팅 대화 인용·닉네임
- 댓글 유도 질문 두 개 이상
