import os, sys, html
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__))
C = f"file://{D}/char"
FD = f"file://{D}/fonts"

CSS = f"""
@font-face{{font-family:Jua;src:url({FD}/jua-korean-400-normal.woff2)}}
@font-face{{font-family:Jua;src:url({FD}/jua-latin-400-normal.woff2);unicode-range:U+0000-00FF}}
@font-face{{font-family:Gowun;src:url({FD}/gowun-dodum-korean-400-normal.woff2)}}
@font-face{{font-family:Gowun;src:url({FD}/gowun-dodum-latin-400-normal.woff2);unicode-range:U+0000-00FF}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;background:#FBFDF7;font-family:Jua,sans-serif;color:#1F3A12;overflow:hidden}}
.page{{position:absolute;inset:0;padding:34px;display:flex;flex-direction:column;gap:22px}}
.pn{{border:5px solid #1F4A0C;background:#fff;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;gap:20px;padding:22px}}
.burst{{background:radial-gradient(circle at 50% 62%,#FFFFFF 0%,#EEF8E4 70%)}}
.lite{{background:#EEF8E4}}
.dark{{background:#1F4A0C;color:#fff}}
.row{{display:flex;gap:22px}}
.row>.pn{{flex:1}}
.tagbox{{position:absolute;top:18px;left:20px;font-size:24px;border:3px solid #1F4A0C;background:#FFE58A;padding:4px 14px;color:#1F4A0C}}
.tagbox.r{{left:auto;right:20px}}
.b{{background:#fff;border:4px solid #1F4A0C;border-radius:28px;padding:16px 24px;font-size:36px;line-height:1.35;position:relative}}
.b.g{{background:#E3F3D2}}
.b.y{{background:#FFF3B8}}
.b.sm{{font-size:30px;padding:12px 20px}}
.who{{font-size:22px;color:#4A6B3A;display:block;margin-bottom:4px}}
.c{{display:block;flex:none}}
.fig{{display:flex;flex-direction:column;align-items:center;gap:6px;flex:none}}
.nt{{font-size:24px;background:#2E8B12;color:#fff;border:3px solid #1F4A0C;border-radius:999px;padding:2px 14px}}
.nt.j{{background:#FFB627;color:#1F3A12}}
.red{{color:#C8452C}}.grn{{color:#2E8B12}}
.big{{font-size:64px;line-height:1.25}}
.mark{{background:linear-gradient(transparent 60%,#C9EBA8 60%)}}
.foot{{display:flex;justify-content:space-between;font-size:24px;color:#4A6B3A}}
.boom{{font-size:54px;border:5px solid #1F4A0C;background:#fff;padding:10px 26px;transform:rotate(-3deg)}}
.step{{display:flex;align-items:center;gap:20px;border:4px solid #1F4A0C;background:#fff;padding:18px 24px;text-align:left}}
.num{{flex:none;width:64px;height:64px;background:#1F4A0C;color:#fff;font-size:36px;display:flex;align-items:center;justify-content:center}}
.step b{{font-weight:400;font-size:36px;display:block}}
.step span{{font-family:Gowun;font-size:27px;color:#46553D}}
.meter{{display:flex;flex-direction:column;gap:12px;width:100%}}
.bar{{display:flex;align-items:center;gap:16px;font-size:30px}}
.bar i{{display:block;height:44px;background:#4CAF1F;border:4px solid #1F4A0C}}
.bar em{{font-style:normal;width:130px;text-align:right}}
"""

JUSUN = {"mental","hello","listening","withdraw","nice","nocustomer"}

def ch(name, w):
    j = name in JUSUN
    src = f"{C}/j_{name}.png" if j else f"{C}/{name}.png"
    tag = ('<span class="nt j">신입 죽순</span>' if j else '<span class="nt">선배 밤부</span>')
    return f'<span class="fig"><img class="c" src="{src}" style="width:{w}px">{tag}</span>'


def br(t):
    return html.escape(t).replace("\n", "<br>")


def bubble(name, text, cls="sm"):
    j = name in JUSUN
    who = "죽순" if j else "밤부"
    return f'<div class="b {cls} {"y" if j else "g"}"><span class="who">{who}</span>{br(text)}</div>'


def slides(e):
    n = e["no"]
    (c1, t1), (c2, t2) = e["cover"]
    s = []
    s.append(f'''<div class="page"><div class="pn burst" style="flex:1;flex-direction:column;justify-content:space-between;padding:56px 40px 30px">
 <div style="background:#fff;border:6px solid #1F4A0C;box-shadow:14px 14px 0 #1F4A0C;padding:34px 40px;text-align:center;transform:rotate(-1.5deg)">
  <div style="font-size:84px;line-height:1.18">{br(e["hook"][0])}</div><div class="red" style="font-size:84px;line-height:1.18">{br(e["hook"][1])}</div></div>
 <div style="font-size:30px;border:3px solid #1F4A0C;background:#fff;padding:4px 18px">{br(e["sub"])}</div>
 <div style="display:flex;align-items:flex-end;gap:50px">
  <div style="display:flex;flex-direction:column;align-items:center;gap:12px">{bubble(c1,t1,"")}{ch(c1,290)}</div>
  <div style="display:flex;flex-direction:column;align-items:center;gap:12px">{bubble(c2,t2,"")}{ch(c2,300)}</div>
 </div>
 <div class="foot" style="width:100%;align-items:center"><span style="border:3px solid #1F4A0C;background:#FFE58A;padding:4px 16px;color:#1F4A0C;font-size:28px">대숲툰 {n}화</span><span class="red" style="font-size:28px">넘겨서 확인 →</span></div>
</div></div>''')
    tc, tt = e["s2_top"]; lc, lb, lcap = e["s2_left"]; rc, rb = e["s2_right"]; bc, bt = e["s2_boom"]
    s.append(f'''<div class="page">
 <div class="pn lite" style="height:330px;justify-content:space-between;padding:60px 40px 20px">
  <span class="tagbox">{br(e["s2_tag"])}</span>{bubble(tc,tt,"")}{ch(tc,220)}</div>
 <div class="row" style="height:440px">
  <div class="pn" style="flex-direction:column;padding:26px">{bubble(lc,lb)}{ch(lc,200)}<div style="font-family:Gowun;font-size:26px;color:#46553D">{br(lcap)}</div></div>
  <div class="pn burst" style="flex-direction:column;padding:26px"><div class="boom red" style="font-size:46px">{br(rb)}</div>{ch(rc,210)}</div>
 </div>
 <div class="pn burst" style="flex:1">{ch(bc,200)}<div class="boom">{br(bt)}</div></div>
</div>''')
    bc3, bt3 = e["s3_bambu"]; l3, lt3 = e["s3_left"]; r3, rt3 = e["s3_right"]
    items = "".join(f'<div style="display:flex;gap:18px;align-items:center;border:4px solid #1F4A0C;background:#F4FAEE;padding:14px 20px"><span style="flex:none;background:#1F4A0C;color:#fff;font-size:30px;padding:4px 14px">{br(a)}</span><span style="font-family:Gowun;font-size:32px">{br(b)}</span></div>' for a, b in e["s3_items"])
    s.append(f'''<div class="page">
 <div class="pn lite" style="height:300px;justify-content:space-between;padding:50px 40px 20px">
  <span class="tagbox r">선배 판다 밤부 등장</span>{ch(bc3,250)}{bubble(bc3,bt3,"")}</div>
 <div class="pn" style="flex:1;flex-direction:column;align-items:stretch;justify-content:center;gap:16px;padding:30px 40px">
  <div style="font-size:42px;margin-bottom:8px;text-align:center"><span class="mark">{br(e["s3_title"])}</span></div>{items}</div>
 <div class="row" style="height:330px">
  <div class="pn" style="padding:20px">{ch(l3,170)}{bubble(l3,lt3)}</div>
  <div class="pn burst" style="padding:20px">{bubble(r3,rt3)}{ch(r3,150)}</div>
 </div>
</div>''')
    steps = "".join(f'<div class="step"{" style=&quot;background:#FFF3B8&quot;" if i==2 else ""}><div class="num">{i+1}</div><div><b>{br(a)}</b><span>{br(b)}</span></div></div>'.replace("&quot;", '"') for i, (a, b) in enumerate(e["tips"]))
    s.append(f'''<div class="page">
 <div class="pn lite" style="height:270px;justify-content:space-between;padding:50px 40px 20px">
  <span class="tagbox">밤부의 한마디</span>{ch("tip",240)}<div class="b g">{br(e["tip_intro"])}</div></div>
 {steps}
 <div class="pn burst" style="flex:1">{ch("empathy",200)}<div class="boom" style="font-size:46px">{br(e["tip_boom"])}</div></div>
</div>''')
    a, b, c = e["sum"]
    s.append(f'''<div class="page">
 <div class="pn dark" style="height:270px;flex-direction:column;align-items:flex-start;justify-content:center;padding:30px 44px">
  <div style="font-size:28px;color:#C9EBA8">오늘의 한 줄 정리</div>
  <div style="font-size:48px;line-height:1.3">{br(a)}<span style="color:#FFD84D">{br(b)}</span>{br(c)}</div></div>
 <div class="row" style="flex:1">
  <div class="pn lite" style="flex-direction:column;padding:26px">{bubble("together",e["sum_bambu"])}{ch("together",240)}</div>
  <div class="pn burst" style="flex-direction:column;padding:26px">{bubble("nice",e["sum_jusun"])}{ch("nice",220)}</div>
 </div>
 <div class="pn" style="height:250px;flex-direction:column;align-items:flex-start;background:#FFF3B8;padding:28px 40px">
  <div style="font-size:36px">{br(e["question"])}</div>
  <div style="font-family:Gowun;font-size:28px;margin-top:14px;color:#46553D">{br(e["next"])}</div></div>
</div>''')
    s.append(f'''<div class="page"><div class="pn burst" style="flex:1;flex-direction:column;gap:28px;padding:50px">
 <div style="font-size:30px;border:3px solid #1F4A0C;background:#FFE58A;padding:6px 22px">대숲툰은 여러분의 이야기로 만들어요</div>
 <div style="background:#fff;border:6px solid #1F4A0C;box-shadow:12px 12px 0 #1F4A0C;padding:30px 44px;text-align:center">
  <div style="font-size:58px;line-height:1.3">웃펐던 그날,<br><span class="grn">밤부에게 외쳐주세요</span></div></div>
 {ch("talk",360)}
 <div class="b g" style="text-align:center">인스타 DM으로 사연 보내기<br><span style="font-family:Gowun;font-size:28px">이름·회사는 지우고 익명으로 다듬어요</span></div>
 <div class="foot" style="width:100%"><span>대나무숲 · 대숲툰</span><span>팔로우하고 다음 화 보기</span></div>
</div></div>''')
    return s


def caption(e):
    n = e["no"]
    hook = " ".join(x.replace("\n", " ") for x in e["hook"])
    tips = "\n".join(f"✔ {a}" for a, _ in e["tips"])
    a, b, c = e["sum"]
    line = (a + b + c).replace("\n", " ").strip()
    return (f"{hook} 🎋\n\n대숲툰 {n}화 · {e['sub'].strip('()')}\n\n{tips}\n\n"
            f"오늘의 한 줄 ▶ {line}\n\n{e['question']} 👇\n{e['next']}\n\n"
            f"💌 웃펐던 그날, DM으로 밤부에게 외쳐주세요 (익명 보장)\n\n"
            f"#대숲툰 #인스타툰 #설계사 #보험설계사 #설계사공감 #영업인 #직장인공감 #대나무숲 {e['tags']}")



def render(spec_path, repo_root):
    import json, subprocess
    from PIL import Image
    e = json.load(open(spec_path, encoding="utf-8"))
    slug = e["slug"]
    out = os.path.join(repo_root, "posts", slug)
    work = os.path.join(repo_root, ".toon_work", slug)
    os.makedirs(out, exist_ok=True); os.makedirs(work, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, sl in enumerate(slides(e), 1):
            h = f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{sl}</body></html>'
            fp = os.path.join(work, f"s{i}.html"); open(fp, "w", encoding="utf-8").write(h)
            pg.goto("file://" + fp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
            png = os.path.join(work, f"{i:02d}.png"); pg.screenshot(path=png)
            im = Image.open(png).convert("RGB"); im.save(os.path.join(out, f"{i:02d}.jpg"), quality=92)
            bg = Image.new("RGB", (1080, 1920), "#E6F5D9"); bg.paste(im, (0, 230)); bg.save(os.path.join(work, f"r{i:02d}.png"))
        b.close()
    Image.open(os.path.join(work, "r01.png")).convert("RGB").save(os.path.join(out, "cover.jpg"), quality=90)
    dur = [3.2, 4.2, 4.2, 4.2, 3.6, 3.0]; t = 0.4; inp = []
    for i, x in enumerate(dur, 1):
        inp += ["-loop", "1", "-t", str(x), "-i", os.path.join(work, f"r{i:02d}.png")]
    f = []; prev = "[0:v]"; off = 0
    for i in range(1, 6):
        off += dur[i-1] - t; o = f"[v{i}]"
        f.append(f"{prev}[{i}:v]xfade=transition=slideleft:duration={t}:offset={off:.2f}{o}"); prev = o
    fc = ";".join(f) + f";{prev}format=yuv420p,fps=30[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-i", os.path.join(D, "bgm.m4a"), "-filter_complex", fc,
                    "-map", "[o]", "-map", "6:a", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", os.path.join(out, "reel.mp4")], check=True)
    post = {"no": int(slug), "slug": slug, "title": f"대숲툰 {e['no']}화 · " + " ".join(e["hook"]).replace("\n", " "),
            "series": "대숲툰", "type": "toon", "images": [f"{i:02d}.jpg" for i in range(1, 7)],
            "video": "reel.mp4", "cover": "cover.jpg", "publish_after": e["date"], "caption": caption(e)}
    json.dump(post, open(os.path.join(out, "post.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("완료", slug, e["date"], os.path.join(work, "01.png"))


if __name__ == "__main__":
    # 사용법: python tools/toon/render.py toon/08.json [toon/09.json ...]
    root = os.path.dirname(os.path.dirname(D))
    for sp in sys.argv[1:]:
        render(sp, root)
