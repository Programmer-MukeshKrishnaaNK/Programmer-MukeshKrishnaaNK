#!/usr/bin/env python3
from __future__ import annotations
import datetime as dt, json, os, urllib.request, urllib.error, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT = ASSETS / "fonts" / "InstrumentSerif-Regular.ttf"
ITALIC = ASSETS / "fonts" / "InstrumentSerif-Italic.ttf"

USERNAME = os.environ.get("GITHUB_USERNAME", "Programmer-MukeshKrishnaaNK")

BG = (248,248,246)
INK = (16,16,16)
MID = (112,112,108)
LIGHT = (218,218,214)
WHITE = (255,255,255)

def font(path, size):
    return ImageFont.truetype(str(path), size)

def mono(size):
    # GitHub runners normally have DejaVu Sans Mono; fallback is PIL default.
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
    ]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def fit_text(draw, text, fnt, max_w):
    # Instrument Serif is display-oriented; shrink until it fits.
    size = fnt.size
    path = FONT
    while draw.textbbox((0,0), text, font=fnt)[2] > max_w and size > 20:
        size -= 2
        fnt = font(path, size)
    return fnt

def api(path):
    token = os.environ.get("GITHUB_TOKEN","")
    req = urllib.request.Request(
        "https://api.github.com" + path,
        headers={
            "Accept":"application/vnd.github+json",
            "Authorization":f"Bearer {token}",
            "X-GitHub-Api-Version":"2022-11-28",
            "User-Agent":"mukesh-github-profile",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def graphql(query, variables):
    token = os.environ.get("GITHUB_TOKEN","")
    body = json.dumps({"query":query, "variables":variables}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Accept":"application/vnd.github+json",
            "Authorization":f"Bearer {token}",
            "Content-Type":"application/json",
            "User-Agent":"mukesh-github-profile",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def save_gif(frames, path, duration=90):
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=duration, loop=0, optimize=True)

def draw_rule(draw, y, x1=70, x2=1130, width=1):
    draw.line((x1,y,x2,y), fill=LIGHT, width=width)

def make_hero():
    W,H=1200,420
    frames=[]
    title="MUKESH"
    sub="KRISHNAA NK"
    for i in range(30):
        im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
        d.text((70,48),"01 / PROFILE",font=mono(16),fill=MID)
        d.text((1060,48),"2026",font=mono(16),fill=MID,anchor="ra")
        draw_rule(d,78)
        # Keep the first frame complete, then add subtle motion so GitHub never
        # shows an empty-looking poster even before the GIF advances.
        f=fit_text(d,title,font(FONT,126),900)
        y_shift = int(2 * math.sin(i/4))
        d.text((68,y_shift+120),title,font=f,fill=INK)
        d.text((70,248),sub,font=font(ITALIC,62),fill=INK)
        # Blinking editorial cursor
        if (i//4)%2==0:
            d.rectangle((70,323,78,335),fill=INK)
        # Moving editorial line
        x=70 + ((i*32) % 780)
        d.line((x,324,x+210,324),fill=INK,width=2)
        d.ellipse((x+214,319,x+224,329),fill=INK)
        d.text((70,352),"student / builder / creative developer",font=mono(16),fill=MID)
        d.text((1130,352),"github.com/Programmer-MukeshKrishnaaNK",font=mono(13),fill=MID,anchor="ra")
        frames.append(im)
    save_gif(frames, ASSETS/"hero.gif", 85)

def make_stats(stats):
    W,H=1200,300
    frames=[]
    labels=[("REPOSITORIES",stats["repos"]),("FOLLOWERS",stats["followers"]),("STARS",stats["stars"])]
    for i in range(32):
        im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
        d.text((70,34),"02 / SIGNAL",font=mono(16),fill=MID)
        d.text((1130,34),"LIVE DATA",font=mono(16),fill=MID,anchor="ra")
        draw_rule(d,64)
        xs=[70,450,830]
        for j,(lab,val) in enumerate(labels):
            x=xs[j]
            d.text((x,90),lab,font=mono(14),fill=MID)
            shown=int(round(val*min(1,max(0,(i-j*4)/16))))
            f=font(FONT,82)
            d.text((x,124),str(shown),font=f,fill=INK)
            # underline grows
            prog=min(1,max(0,(i-4-j*3)/18))
            d.line((x,225,x+280*prog,225),fill=INK,width=3)
            d.ellipse((x+280*prog-3,222,x+280*prog+3,228),fill=INK)
        d.text((70,260),f"updated {stats['updated']}",font=mono(13),fill=MID)
        frames.append(im)
    save_gif(frames, ASSETS/"stats.gif", 95)

def make_projects():
    projects=[
      ("Smart Restaurant Reservation Website System","HTML"),
      ("The Midnight Library","AI / WEB"),
      ("ether-lofi-experience","MOTION / WEB"),
      ("Cafe Theme Page","ANIMATION"),
      ("Portfolio","TYPESCRIPT"),
      ("metrics-dashboard-build","DASHBOARD"),
    ]
    W,H=1200,360
    frames=[]
    for i in range(42):
        im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
        d.text((70,34),"03 / WORK",font=mono(16),fill=MID)
        d.text((1130,34),"SELECTED PUBLIC PROJECTS",font=mono(13),fill=MID,anchor="ra")
        draw_rule(d,64)
        idx=(i//7)%len(projects)
        title,tag=projects[idx]
        phase=(i%7)/7
        # slide/fade feel via x offset
        off=int((1-phase)*55)
        d.text((70+off,108),title,font=font(FONT,62),fill=INK)
        d.text((72,184),tag,font=mono(15),fill=MID)
        d.text((72,230),"published work / interface experiments / tools",font=mono(14),fill=MID)
        # index rail
        for j in range(len(projects)):
            x=70+j*42
            active=(j==idx)
            d.rectangle((x,295,x+26,299),fill=INK if active else LIGHT)
        d.text((1130,280),f"{idx+1:02d} / {len(projects):02d}",font=mono(14),fill=MID,anchor="ra")
        frames.append(im)
    save_gif(frames, ASSETS/"projects.gif", 105)

def make_contrib(days, total):
    W,H=1200,300
    frames=[]
    # last 52 weeks x 7 days
    vals=[d["contributionCount"] for w in days for d in w["contributionDays"]]
    vals=vals[-364:] if len(vals)>=364 else vals
    vals=( [0]*(364-len(vals)) + vals )
    grid=[vals[c*7:(c+1)*7] for c in range(52)]
    maxv=max(vals) if vals else 1
    for i in range(28):
        im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
        d.text((70,34),"04 / ACTIVITY",font=mono(16),fill=MID)
        d.text((1130,34),f"{total} CONTRIBUTIONS",font=mono(13),fill=MID,anchor="ra")
        draw_rule(d,64)
        cell=15; gap=4; x0=70; y0=100
        progress=min(1,i/18)
        for c,col in enumerate(grid):
            for r,v in enumerate(col):
                threshold=(c*7+r)/364
                if threshold <= progress:
                    level=min(4,int((v/maxv)*4)+1) if v else 0
                else: level=0
                # monochrome levels
                fills=[BG,(232,232,228),(190,190,185),(110,110,105),INK]
                x=x0+c*(cell+gap); y=y0+r*(cell+gap)
                d.rounded_rectangle((x,y,x+cell,y+cell),radius=3,fill=fills[level])
        d.text((70,265),"quietly building, one contribution at a time",font=font(ITALIC,25),fill=INK)
        # Always animate a subtle sweep, even when the account has a quiet week.
        sx = 70 + int((1060 * ((i % 20) / 19)))
        d.line((sx,88,sx+46,88),fill=INK,width=2)
        frames.append(im)
    save_gif(frames, ASSETS/"contributions.gif", 100)

def main():
    # Safe fallback values if API is unavailable during a local preview.
    repos_n, followers, stars = 7, 0, 0
    total=0; weeks=[]
    try:
        user=api(f"/users/{USERNAME}")
        repos=api(f"/users/{USERNAME}/repos?per_page=100&sort=updated")
        repos_n=user.get("public_repos",0)
        followers=user.get("followers",0)
        stars=sum(r.get("stargazers_count",0) for r in repos)
    except Exception:
        pass
    try:
        q="""query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions,weeks{contributionDays{contributionCount,date}}}}}}"""
        out=graphql(q,{"login":USERNAME})
        cal=out["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        total=cal["totalContributions"]; weeks=cal["weeks"]
    except Exception:
        weeks=[{"contributionDays":[{"contributionCount":0,"date":""} for _ in range(7)]} for _ in range(52)]
    stats={"repos":repos_n,"followers":followers,"stars":stars,"updated":dt.date.today().isoformat()}
    make_hero(); make_stats(stats); make_projects(); make_contrib(weeks,total)

if __name__=="__main__":
    main()
