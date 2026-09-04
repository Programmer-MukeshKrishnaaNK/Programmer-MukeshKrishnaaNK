#!/usr/bin/env python3
import json, os, re, urllib.request
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
USERNAME = os.getenv('GITHUB_USERNAME', 'Programmer-MukeshKrishnaaNK')

# Keep the font inside the SVG so GitHub doesn't need to fetch a web font.
def b64(path):
    import base64
    return base64.b64encode(path.read_bytes()).decode()

FONT = b64(ROOT / 'fonts' / 'InstrumentSerif-Regular.woff2')
ITALIC = b64(ROOT / 'fonts' / 'InstrumentSerif-Italic.woff2')
FONT_CSS = (
    "@font-face{font-family:InstrumentSerif;src:url(data:font/woff2;base64," + FONT + ") format('woff2');font-weight:400}"
    "@font-face{font-family:InstrumentSerif;src:url(data:font/woff2;base64," + ITALIC + ") format('woff2');font-style:italic;font-weight:400}"
)

STYLE = f'''<style>{FONT_CSS}
.serif{{font-family:InstrumentSerif,Georgia,serif}} .mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
.muted{{fill:#6b6b6b}} .ink{{fill:#111}} .line{{stroke:#111;stroke-width:1}}
</style>'''

def wrap(body, w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{STYLE}{body}</svg>'

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent':'Mukesh-GitHub-Profile'})
    token = os.getenv('GITHUB_TOKEN')
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def github_stats():
    try:
        user = fetch_json(f'https://api.github.com/users/{USERNAME}')
        repos = []
        page = 1
        while page <= 5:
            data = fetch_json(f'https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}&type=owner')
            if not data: break
            repos.extend(data)
            if len(data) < 100: break
            page += 1
        return {
            'repos': user.get('public_repos', len(repos)),
            'followers': user.get('followers', 0),
            'stars': sum(r.get('stargazers_count', 0) for r in repos),
        }
    except Exception:
        return {'repos':'—','followers':'—','stars':'—'}

def contributions():
    # GitHub's public contribution page is enough for a self-hosted profile graphic.
    try:
        req = urllib.request.Request(
            f'https://github.com/users/{USERNAME}/contributions',
            headers={'User-Agent':'Mukesh-GitHub-Profile'}
        )
        html = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'ignore')
        vals = [int(x) for x in re.findall(r'data-level="(\d+)"', html)]
        # 364 cells = 52 weeks x 7 days; GitHub may return slightly more depending on range.
        return (vals[-364:] if len(vals) >= 364 else [0]*364)
    except Exception:
        return [0]*364

def bar(value, scale=10):
    try:
        return max(8, min(656, int(float(value) * scale)))
    except Exception:
        return 40

def make_hero():
    body='''
<rect width="724" height="300" fill="#fff"/>
<text x="24" y="28" class="mono muted" font-size="11" letter-spacing="2">PROFILE / 2026</text>
<text x="24" y="105" class="serif ink" font-size="72" opacity="0">MUKESH KRISHNAA
 <animate attributeName="opacity" values="0;1" begin="0.1s" dur="0.55s" fill="freeze"/>
 <animateTransform attributeName="transform" type="translate" values="0 14;0 0" begin="0.1s" dur="0.65s" fill="freeze"/>
</text>
<text x="24" y="166" class="serif" font-size="58" font-style="italic" opacity="0">developer / builder
 <animate attributeName="opacity" values="0;1" begin="0.75s" dur="0.55s" fill="freeze"/>
 <animateTransform attributeName="transform" type="translate" values="0 12;0 0" begin="0.75s" dur="0.65s" fill="freeze"/>
</text>
<line x1="24" y1="191" x2="24" y2="191" class="line"><animate attributeName="x2" from="24" to="680" begin="1.35s" dur="0.9s" fill="freeze"/></line>
<text x="24" y="222" class="mono muted" font-size="12">python · typescript · sql · interfaces · motion</text>
<text x="24" y="265" class="mono ink" font-size="12">$ ./build_profile</text>
<rect x="143" y="254" width="7" height="15" class="ink" opacity="0"><animate attributeName="opacity" values="0;0.8;0" dur="1s" begin="1.7s" repeatCount="indefinite"/></rect>
<g transform="translate(666 38)"><circle cx="0" cy="0" r="14" fill="none" stroke="#111"/><path d="M0 -8 L0 8 M-8 0 L8 0" stroke="#111"/><animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="8s" repeatCount="indefinite"/></g>
'''
    (ASSETS/'hero.svg').write_text(wrap(body,724,300), encoding='utf-8')

def make_stack():
    body='''<rect width="724" height="245" fill="#fff"/>
<text x="24" y="42" class="serif ink" font-size="38">stack</text>
<text x="24" y="64" class="mono muted" font-size="11">things I actually build with</text>
<g class="mono ink" font-size="14">
<text x="24" y="105" opacity="0">PYTHON<tspan class="muted"> / automation, data, tooling</tspan><animate attributeName="opacity" from="0" to="1" begin="0.2s" dur="0.4s" fill="freeze"/></text>
<text x="24" y="135" opacity="0">TYPESCRIPT<tspan class="muted"> / interfaces, web apps</tspan><animate attributeName="opacity" from="0" to="1" begin="0.45s" dur="0.4s" fill="freeze"/></text>
<text x="24" y="165" opacity="0">SQL<tspan class="muted"> / data, queries, systems</tspan><animate attributeName="opacity" from="0" to="1" begin="0.7s" dur="0.4s" fill="freeze"/></text>
<text x="24" y="195" opacity="0">FIGMA + MOTION<tspan class="muted"> / product, interaction</tspan><animate attributeName="opacity" from="0" to="1" begin="0.95s" dur="0.4s" fill="freeze"/></text></g>
<line x1="24" y1="220" x2="24" y2="220" class="line"><animate attributeName="x2" from="24" to="680" begin="1.2s" dur="0.8s" fill="freeze"/></line>'''
    (ASSETS/'stack.svg').write_text(wrap(body,724,245), encoding='utf-8')

def make_projects():
    projects=[
        ('Smart Restaurant Reservation Website System','HTML'),
        ('ether-lofi-experience','web / motion'),
        ('The Midnight Library','AI / web'),
        ('Cafe Theme Page','web / animation'),
        ('Portfolio-','TypeScript'),
        ('metrics-dashboard-build','dashboard'),
    ]
    body='''<rect width="724" height="365" fill="#fff"/><text x="24" y="42" class="serif ink" font-size="38">projects</text><text x="24" y="64" class="mono muted" font-size="11">published work / no placeholders</text>'''
    for i,(name,tag) in enumerate(projects):
        y=95+i*42; d=0.25+i*0.18
        body += f'''<g opacity="0"><text x="24" y="{y}" class="serif ink" font-size="21">{escape(name)}</text><text x="680" y="{y}" class="mono muted" font-size="10" text-anchor="end">{escape(tag)}</text><line x1="24" y1="{y+10}" x2="680" y2="{y+10}" class="line"/><animate attributeName="opacity" from="0" to="1" begin="{d:.2f}s" dur="0.45s" fill="freeze"/></g>'''
    (ASSETS/'projects.svg').write_text(wrap(body,724,365), encoding='utf-8')

def make_stats():
    s=github_stats(); repos=s['repos']; followers=s['followers']; stars=s['stars']
    body=f'''<rect width="724" height="270" fill="#fff"/><text x="24" y="44" class="serif ink" font-size="38">stats</text><text x="24" y="67" class="mono muted" font-size="11">generated from GitHub / updated by action</text>
<g class="mono ink"><text x="24" y="116" font-size="13">PUBLIC REPOS</text><text x="680" y="116" font-size="30" text-anchor="end">{repos}</text><rect x="24" y="128" width="656" height="2" fill="#111" opacity="0.12"/><rect x="24" y="128" width="0" height="2" fill="#111"><animate attributeName="width" from="0" to="{bar(repos,28)}" begin="0.35s" dur="0.9s" fill="freeze"/></rect>
<text x="24" y="171" font-size="13">FOLLOWERS</text><text x="680" y="171" font-size="30" text-anchor="end">{followers}</text><rect x="24" y="183" width="656" height="2" fill="#111" opacity="0.12"/><rect x="24" y="183" width="0" height="2" fill="#111"><animate attributeName="width" from="0" to="{bar(followers,16)}" begin="0.65s" dur="0.9s" fill="freeze"/></rect>
<text x="24" y="226" font-size="13">STARS</text><text x="680" y="226" font-size="30" text-anchor="end">{stars}</text><rect x="24" y="238" width="656" height="2" fill="#111" opacity="0.12"/><rect x="24" y="238" width="0" height="2" fill="#111"><animate attributeName="width" from="0" to="{bar(stars,40)}" begin="0.95s" dur="0.9s" fill="freeze"/></rect></g>'''
    (ASSETS/'stats.svg').write_text(wrap(body,724,270), encoding='utf-8')

def make_contrib():
    vals=contributions()
    cells=[]
    # 52 columns, 7 rows; subtle staggered reveal like the reference SVG.
    shades=['#f1f1f1','#d8d8d8','#bdbdbd','#777','#111']
    for i,v in enumerate(vals):
        col=i//7; row=i%7
        x=24+col*12.5; y=76+row*9.2
        shade=shades[min(4,max(0,v))]
        delay=1.0 + i*0.012
        cells.append(f'''<rect x="{x:.1f}" y="{y:.1f}" width="9" height="6" rx="1" fill="{shade}" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.12s" fill="freeze"/></rect>''')
    body='''<rect width="724" height="150" fill="#fff"/><text x="24" y="38" class="serif ink" font-size="34">activity</text><text x="24" y="58" class="mono muted" font-size="10">contribution rhythm / last 52 weeks</text>''' + ''.join(cells)
    (ASSETS/'contributions.svg').write_text(wrap(body,724,150), encoding='utf-8')

def main():
    ASSETS.mkdir(exist_ok=True)
    make_hero(); make_stack(); make_projects(); make_stats(); make_contrib()
    print('Generated profile SVGs for', USERNAME)

if __name__ == '__main__':
    main()
