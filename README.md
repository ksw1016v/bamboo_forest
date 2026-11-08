# 대나무숲 (bamboo_forest)

설계사를 위한 공감·소통·성장 커뮤니티 **대나무숲** 인스타그램 자동 게시 + 홈페이지.

## 홈페이지 (GitHub Pages)
- `index.html` 메인 (인스타 프로필 링크용) — 오픈채팅·인스타 주소는 파일 아래쪽 `LINKS`에 입력
- `privacy.html` 개인정보처리방침 · `terms.html` 이용약관 · `data-deletion.html` 데이터 삭제 안내 (Meta 앱 설정용)

## 자동 게시 (GitHub Actions)
- `posts/NNN/post.json` 게시물 원고 + 이미지(JPG)·영상. 번호 순서대로 하루 1편, 매일 19:00(KST) 게시
- `publish.py` 인스타그램 API 게시 · 게시 기록은 `state.json`
- `guard.py` 하루 1편 제한
- 워크플로: `daily-post`(자동/수동 게시), `check-connection`(토큰 연결 확인), `refresh-token`(매달 토큰 연장)

## Secrets (Settings → Secrets and variables → Actions)
- `IG_TOKEN` 인스타그램 장기 액세스 토큰
- `IG_USER_ID` 인스타그램 사용자 ID (Instagram 로그인 토큰이면 생략 가능)
