# 대나무숲 원고 스킬

대숲툰·게시물 원고, 캡션, 댓글, DM을 쓸 때 쓰는 클로드 스킬 5개입니다. **모두 글만 쓰고, 게시·발송은 하지 않습니다.**
모든 스킬은 `toon/TOON_GUIDE.md` 의 '글쓰기 원칙'과 '콘텐츠 기준'을 먼저 따릅니다.

| 명령 | 하는 일 |
|---|---|
| `/bf-hook` | 대숲툰 표지 hook·캡션 첫 줄 후보 3개를 공식별로 쓰고 점수 매기기 |
| `/bf-caption` | 대숲툰 캡션 형식대로 쓰기 → `caption_check.py` 로 점검 |
| `/bf-human` | AI 티 나는 말투·문자 지우기 |
| `/bf-reply` | 댓글(공감·고민·질문)을 분류하고 밤부 말투로 답글 초안 쓰기 |
| `/bf-dm` | 사연 DM 답장, 사연 소개 동의 요청, 오픈채팅 안내 문구 쓰기 |

자동 점검: `publish.py` 가 게시 직전에 `caption_check.py` 를 돌려 문제를 Actions 경고로 남깁니다(게시는 막지 않음).
직접 점검: `python3 caption_check.py --all`

---
아이디어 출처: [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)
(MIT License, Copyright (c) Jake Schincariol). 대나무숲 계정에 맞게 새로 작성했습니다.
