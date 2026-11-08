"""posts/ 대기열에서 아직 안 올린 다음 게시물을 골라 인스타그램에 게시한다.

posts/NNN/post.json
  type: "carousel"(images 2~10장) | "image"(images 1장) | "reel"(video, cover 선택)
  caption: 캡션
  publish_after (선택): "2026-11-12" 이 날짜 전에는 올리지 않음

환경변수
  IG_TOKEN     인스타그램 장기 액세스 토큰 (GitHub Secrets)
  IG_USER_ID   인스타그램 사용자 ID (GitHub Secrets, 없으면 토큰으로 자동 조회)
  MEDIA_BASE   미디어 공개 주소 접두사 (워크플로가 자동 설정)
  DRY_RUN=1    실제 게시 없이 확인만

사용법
  python publish.py next          -> 다음 게시물 slug 출력 (없으면 빈 줄)
  python publish.py post <slug>   -> 게시 후 state.json 갱신
  python publish.py check         -> 토큰 연결 확인 (계정 이름 출력)
"""
import datetime, json, os, pathlib, sys, time, urllib.error, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).parent
STATE = ROOT / "state.json"
KST = datetime.timezone(datetime.timedelta(hours=9))


def api_base():
    tok = os.environ.get("IG_TOKEN", "")
    return "https://graph.instagram.com/v23.0" if tok.startswith("IG") else "https://graph.facebook.com/v23.0"


def call(method, path, **params):
    params["access_token"] = os.environ["IG_TOKEN"]
    data = urllib.parse.urlencode(params).encode()
    url = f"{api_base()}/{path}"
    req = urllib.request.Request(url + "?" + data.decode()) if method == "GET" else urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"::error::API 오류 {e.code} ({path.split('/')[-1] or path}): {body[:400]}")
        raise SystemExit(f"API 오류 {e.code} {path}: {body}")


def user_id():
    uid = os.environ.get("IG_USER_ID", "").strip()
    if uid:
        return uid
    if api_base().startswith("https://graph.instagram.com"):
        return call("GET", "me", fields="user_id")["user_id"]
    print("::error::Facebook 로그인 토큰(EAA...)은 IG_USER_ID 시크릿이 꼭 필요해요.")
    raise SystemExit("IG_USER_ID 시크릿이 필요해요.")


def load_state():
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"published": [], "log": []}


def save_state(st):
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def posts():
    for f in sorted((ROOT / "posts").glob("*/post.json")):
        yield f.parent.name, json.loads(f.read_text(encoding="utf-8"))


def next_post():
    done = set(load_state()["published"])
    today = datetime.datetime.now(KST).date().isoformat()
    for slug, p in posts():
        if slug in done or p.get("skip"):
            continue
        if p.get("publish_after", "") > today:
            continue
        return slug
    return None


def wait_ready(cid, tries=40):
    for _ in range(tries):
        st = call("GET", cid, fields="status_code")["status_code"]
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise SystemExit(f"컨테이너 {cid} 상태 {st}")
        time.sleep(5)
    raise SystemExit(f"컨테이너 {cid} 준비 시간 초과")


def post(slug):
    p = json.loads((ROOT / "posts" / slug / "post.json").read_text(encoding="utf-8"))
    base = os.environ["MEDIA_BASE"].rstrip("/") + f"/posts/{slug}"
    kind = p["type"]
    if os.environ.get("DRY_RUN"):
        print("DRY RUN", slug, kind, base, p["caption"][:60])
        return
    uid = user_id()
    print("계정:", call("GET", uid, fields="username").get("username"))
    if kind == "reel":
        extra = {"cover_url": f"{base}/{p['cover']}"} if p.get("cover") else {"thumb_offset": "1000"}
        cid = call("POST", f"{uid}/media", media_type="REELS", video_url=f"{base}/{p['video']}",
                   caption=p["caption"], share_to_feed="true", **extra)["id"]
        wait_ready(cid, tries=72)
    elif kind == "image":
        cid = call("POST", f"{uid}/media", image_url=f"{base}/{p['images'][0]}", caption=p["caption"])["id"]
        wait_ready(cid)
    else:
        kids = [call("POST", f"{uid}/media", image_url=f"{base}/{im}", is_carousel_item="true")["id"] for im in p["images"]]
        for k in kids:
            wait_ready(k)
        cid = call("POST", f"{uid}/media", media_type="CAROUSEL", children=",".join(kids), caption=p["caption"])["id"]
        wait_ready(cid)
    res = call("POST", f"{uid}/media_publish", creation_id=cid)
    print("게시 완료 media id:", res["id"])
    st = load_state()
    st["published"].append(slug)
    st["log"].append({"slug": slug, "type": kind, "media_id": res["id"],
                      "at": datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")})
    save_state(st)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "next"
    if cmd == "next":
        print(next_post() or "")
    elif cmd == "post":
        post(sys.argv[2])
    elif cmd == "check":
        tok = os.environ.get("IG_TOKEN", "").strip()
        has_uid = bool(os.environ.get("IG_USER_ID", "").strip())
        kind = "Instagram 로그인(IG...)" if tok.startswith("IG") else ("Facebook 로그인(EAA...)" if tok.startswith("EAA") else "알 수 없음")
        print(f"::notice::토큰 {'있음' if tok else '없음'} · 종류 {kind} · 길이 {len(tok)} · IG_USER_ID {'있음' if has_uid else '없음'}")
        if not tok:
            print("::error::IG_TOKEN 시크릿이 비어 있어요. Settings → Secrets and variables → Actions 에서 이름을 정확히 IG_TOKEN 으로 넣어주세요.")
            sys.exit(1)
        if tok != os.environ["IG_TOKEN"]:
            print("::warning::토큰 앞뒤에 공백이나 줄바꿈이 있어요. 시크릿을 다시 붙여넣어 주세요.")
            os.environ["IG_TOKEN"] = tok
        uid = user_id()
        name = call("GET", uid, fields="username").get("username")
        print(f"::notice::연결 확인 성공: @{name}")
