"""하루 1편 원칙: 오늘(한국시간) 이미 올렸거나 아직 게시 시간 전이면 skip=1.
GitHub 예약 실행은 늦거나 겹칠 수 있어 목표 시각 이후 여러 번 실행하고, 처음 조건을 만족한 실행만 올린다.
수동 실행(workflow_dispatch)은 시간 제한 없이 진행(하루 1편 제한도 force 입력으로 해제 가능)."""
import datetime, json, os, pathlib

TARGET = (19, 0)   # 매일 19:00 KST 목표
EARLY = datetime.timedelta(minutes=15)
KST = datetime.timezone(datetime.timedelta(hours=9))

now = datetime.datetime.now(KST).replace(tzinfo=None)
st = pathlib.Path(__file__).parent / "state.json"
log = json.loads(st.read_text(encoding="utf-8")).get("log", []) if st.exists() else []
manual = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"
force = os.environ.get("FORCE") == "true"
skip = 0
if not force and any(e["at"][:10] == now.date().isoformat() for e in log):
    skip = 1
if not manual and now < datetime.datetime.combine(now.date(), datetime.time(*TARGET)) - EARLY:
    skip = 1
print(f"skip={skip}")
