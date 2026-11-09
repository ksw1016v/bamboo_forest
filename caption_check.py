"""캡션 점검기 (대나무숲) — 게시 전에 캡션이 계정 규칙에 맞는지 확인한다.

게시를 막지는 않는다. 문제를 찾으면 GitHub Actions 화면에 경고(노란 줄)로 남긴다.
규칙 출처: toon/TOON_GUIDE.md '콘텐츠 기준'·'글쓰기 원칙'
(아이디어 출처: Jakeschincariol/instagram-agent-skill 의 caption.py·detect.py, MIT.
 대나무숲 계정 규칙에 맞게 새로 작성함)

사용법
  python3 caption_check.py posts/005/post.json      한 편 점검
  python3 caption_check.py --all                    아직 안 올린 게시물 전부 점검
  python3 caption_check.py --all --published        이미 올린 것까지 전부
"""
import json, os, re, sys, pathlib

ROOT = pathlib.Path(__file__).parent
LIMIT = 2200
HOOK_MAX = 70          # '더 보기' 전에 보이는 첫 두 줄 권장 길이(한글 기준 대략값)
TAG_MIN, TAG_MAX = 5, 12
MUST_TAG = "#대나무숲"

# TOON_GUIDE '넣지 않는 것' — 광고심의 대상이 되는 표현
BANNED = {
    "보험료": "보험료 언급 금지", "보험금": "보험금·청구 언급 금지", "청구": "보험금 청구 언급 금지",
    "고지의무": "고지의무 언급 금지", "세액공제": "세액공제 언급 금지", "수수료": "수수료 언급 금지",
    "가입하세요": "가입 권유 금지", "가입 권유": "가입 권유 금지", "보장 내용": "보장 내용 언급 금지",
    "실손": "특정 상품 언급 금지", "종신보험": "특정 상품 언급 금지", "암보험": "특정 상품 언급 금지",
    "연금보험": "특정 상품 언급 금지", "운전자보험": "특정 상품 언급 금지", "치아보험": "특정 상품 언급 금지",
}
INSURERS = ["삼성생명", "한화생명", "교보생명", "신한라이프", "NH농협생명", "농협생명", "미래에셋생명",
            "동양생명", "흥국생명", "ABL생명", "KB라이프", "라이나", "AIA", "메트라이프", "푸르덴셜",
            "삼성화재", "현대해상", "DB손해보험", "DB손보", "KB손해보험", "KB손보", "메리츠", "한화손해보험",
            "흥국화재", "롯데손해보험", "MG손해보험", "AXA", "에이플러스", "GA코리아", "인카금융",
            "글로벌금융", "리치앤코", "프라임에셋"]
# 고객 비하·실적 압박 (경고)
TONE = ["진상", "호구", "블랙컨슈머", "실적 못 채우면", "꼴찌", "무능"]

FINGERPRINT = {
    "—": "긴 줄표(—)", "–": "중간 줄표(–)",
    "​": "보이지 않는 문자(ZWSP)", "‌": "보이지 않는 문자(ZWNJ)",
    "﻿": "보이지 않는 문자(BOM)", " ": "줄바꿈 안 되는 공백",
}
SLOP = ["결론적으로", "요약하자면", "다양한 측면", "중요한 역할을 합니다", "살펴보겠습니다",
        "알아보겠습니다", "핵심은 바로", "여정", "게임 체인저"]

TAG_RE = re.compile(r"#[0-9A-Za-z_가-힣]+")


def check(text):
    out = []
    add = lambda lv, k, msg: out.append((lv, k, msg))
    text = text or ""
    if not text.strip():
        return [("ERROR", "캡션", "캡션이 비어 있어요")]
    if len(text) > LIMIT:
        add("ERROR", "길이", f"{len(text)}자 — 인스타 한도 {LIMIT}자를 넘어요")

    body = TAG_RE.sub("", text)  # 해시태그 안의 단어는 금지어 검사에서 제외
    for w, why in BANNED.items():
        if w in body:
            add("ERROR", "금지 표현", f"'{w}' — {why}")
    for w in INSURERS:
        if w in body:
            add("ERROR", "금지 표현", f"'{w}' — 보험사·회사명 언급 금지")
    for w in TONE:
        if w in body:
            add("WARN", "말투", f"'{w}' — 고객 비하·실적 압박으로 읽힐 수 있어요")

    lines = text.split("\n")
    head = "\n".join(lines[:2]).strip()
    first = lines[0].strip()
    if not first:
        add("WARN", "첫 줄", "첫 줄이 비어 있어요")
    if first.startswith("#"):
        add("WARN", "첫 줄", "해시태그로 시작해요")
    if re.match(r"^(안녕하세요|오늘은)", first):
        add("WARN", "첫 줄", "인사로 시작해요. 공감 멘트나 상황으로 바로 들어가 주세요")
    if len(head) > HOOK_MAX:
        add("WARN", "첫 두 줄", f"{len(head)}자 — '더 보기' 전에 잘릴 수 있어요(권장 {HOOK_MAX}자 이내)")
    if TAG_RE.search(head):
        add("WARN", "첫 두 줄", "해시태그가 '더 보기' 앞에 보여요")

    tags = TAG_RE.findall(text)
    if len(tags) > 30:
        add("ERROR", "해시태그", f"{len(tags)}개 — 인스타 한도 30개 초과")
    elif not (TAG_MIN <= len(tags) <= TAG_MAX):
        add("WARN", "해시태그", f"{len(tags)}개 — 권장 {TAG_MIN}~{TAG_MAX}개")
    if MUST_TAG not in tags:
        add("WARN", "해시태그", f"{MUST_TAG} 태그가 없어요")
    dup = sorted({t for t in tags if tags.count(t) > 1})
    if dup:
        add("WARN", "해시태그", "중복: " + " ".join(dup))

    if "👇" not in text and "댓글" not in text:
        add("WARN", "댓글 유도", "댓글 유도 문장이 없어요")
    if "DM" not in text and "사연" not in text:
        add("WARN", "사연 접수", "사연 접수 안내(💌 DM)가 없어요")

    for ch, name in FINGERPRINT.items():
        if ch in text:
            add("WARN", "AI 흔적", f"{name} {text.count(ch)}개")
    slop = [s for s in SLOP if s in text]
    if slop:
        add("WARN", "AI 말투", "상투어: " + ", ".join(slop))
    return out


def check_post(p):
    r = check(p.get("caption", ""))
    if "reel_caption" in p:
        r += [(lv, "릴스 " + k, m) for lv, k, m in check(p["reel_caption"])]
    return r


def report(path, results):
    gh = os.environ.get("GITHUB_ACTIONS") == "true"
    rel = os.path.relpath(path, ROOT)
    if not results:
        print(f"PASS  {rel}")
        return
    for lv, k, msg in results:
        if gh:
            print(f"::warning file={rel}::[캡션 {'오류' if lv == 'ERROR' else '주의'}] {k}: {msg}")
        else:
            print(f"{lv:5} {rel}  {k}: {msg}")


def warn_only(path):
    """publish.py 에서 호출 — 어떤 경우에도 예외를 밖으로 던지지 않는다."""
    try:
        p = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
        report(path, check_post(p))
    except Exception as e:
        print(f"::warning::캡션 점검을 건너뜀 ({e})")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--all" in sys.argv:
        done = set()
        if "--published" not in sys.argv and (ROOT / "state.json").exists():
            done = set(json.loads((ROOT / "state.json").read_text()).get("published", []))
        files = [f for f in sorted(ROOT.glob("posts/*/post.json")) if f.parent.name not in done]
    else:
        files = [pathlib.Path(a).resolve() for a in args]
    if not files:
        print(__doc__)
    for f in files:
        report(f, check_post(json.loads(f.read_text(encoding="utf-8"))))
