#!/usr/bin/env python3
"""Build the static portfolio from content/site.json.

Writes the committed pages (index.html, 404.html, projects/*/index.html,
sitemap.xml, robots.txt) and a disposable dist/ preview with only the public
files. Standard library only.
"""
import html
import json
import pathlib
import shutil
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://akshayalgox.github.io"
SITE = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))
P = SITE["profile"]
E = html.escape

IMG_SIZES = {}  # name -> {width: (w, h)}, filled from assets/img


def scan_images():
    for f in sorted((ROOT / "assets/img").glob("*.webp")):
        name, _, w = f.stem.rpartition("-")
        data = f.read_bytes()
        # VP8/VP8L/VP8X header parsing for intrinsic size
        fmt = data[12:16]
        if fmt == b"VP8 ":
            width = int.from_bytes(data[26:28], "little") & 0x3FFF
            height = int.from_bytes(data[28:30], "little") & 0x3FFF
        elif fmt == b"VP8L":
            b = int.from_bytes(data[21:25], "little")
            width, height = (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
        else:  # VP8X
            width = int.from_bytes(data[24:27], "little") + 1
            height = int.from_bytes(data[27:30], "little") + 1
        IMG_SIZES.setdefault(name, {})[int(w)] = (width, height)


def img(name, alt, sizes="(min-width: 900px) 50vw, 100vw", cls="", eager=False):
    variants = IMG_SIZES[name]
    widths = sorted(variants)
    w, h = variants[widths[-1]]
    srcset = ", ".join(f"/assets/img/{name}-{x}.webp {x}w" for x in widths)
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="/assets/img/{name}-{widths[-1]}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{E(alt, quote=True)}" {loading}>')


def source_url(p, path):
    kind = "tree" if path in ("src", "tests") or path.endswith("/mocked") else "blob"
    return f"https://github.com/AkshayAlgoX/{p['repo']}/{kind}/{p['sha']}/{quote(path, safe='/')}"


# One small, consistently drawn chevron, used only where direction helps
# (back to the list, on to the next project). Decorative: hidden from screen readers.
def chevron(direction="right"):
    d = "M6 3l5 5-5 5" if direction == "right" else "M10 3L5 8l5 5"
    return (f'<svg class="chev" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false">'
            f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ---------------------------------------------------------------- figures
# Small inline SVG explanations. They illustrate how an algorithm works; they
# are labelled as illustrations and never stand in for real output.


def fig_cashflow():
    # Balance over 30 days: paying today dips under the minimum on day 19;
    # paying on day 12 stays above it. Illustrative numbers.
    W, H, x0, y0 = 520, 250, 40, 58
    def X(d): return x0 + d * 15.5
    def Y(v): return y0 + (60 - v) * 2.6
    base = [(0, 42), (5, 40), (6, 52), (11, 49), (12, 48), (18, 46), (19, 24), (24, 22), (25, 44), (30, 41)]
    now = [(d, v - 14) for d, v in base]
    later = [(d, v - (14 if d >= 12 else 0)) for d, v in base]
    path = lambda pts: " ".join(f"{'M' if i == 0 else 'L'}{X(d):.0f},{Y(v):.0f}" for i, (d, v) in enumerate(pts))
    return f'''<svg class="fig" viewBox="0 0 {W} {H}" role="img" aria-labelledby="cf-t cf-d">
<title id="cf-t">Why the payment day matters</title>
<desc id="cf-d">Projected balance over 30 days. Paying the full amount today drops the balance below the minimum on day 19, when rent is due. Paying on day 12 keeps every later day above the minimum.</desc>
<line x1="40" y1="16" x2="64" y2="16" class="f-good"/><text x="70" y="20" class="f-small">pay on day 12: stays above the minimum</text>
<line x1="40" y1="36" x2="64" y2="36" class="f-bad"/><text x="70" y="40" class="f-small">pay today: drops below it on day 19</text>
<line x1="{x0}" y1="{Y(16):.0f}" x2="{X(30):.0f}" y2="{Y(16):.0f}" class="f-floor"/>
<text x="{X(30):.0f}" y="{Y(16)+15:.0f}" text-anchor="end" class="f-small">minimum balance</text>
<path d="{path(now)}" class="f-bad"/>
<path d="{path(later)}" class="f-good"/>
<circle cx="{X(19):.0f}" cy="{Y(10):.0f}" r="5" class="f-bad-dot"/>
<line x1="{x0}" y1="{Y(0):.0f}" x2="{X(30):.0f}" y2="{Y(0):.0f}" class="f-axis"/>
<text x="{x0}" y="{Y(0)+16:.0f}" class="f-small">today</text><text x="{X(30):.0f}" y="{Y(0)+16:.0f}" text-anchor="end" class="f-small">day 30</text>
</svg>
<p class="fig-cap">Illustration with made-up numbers: the engine checks the lowest balance from each candidate day onward.</p>'''


def fig_subset():
    inv = [("INV-104", "12,000", True), ("INV-109", "18,500", True), ("INV-112", "21,300", False), ("INV-117", "17,700", True), ("INV-121", "9,900", False)]
    rows = ""
    for i, (name, amt, sel) in enumerate(inv):
        y = 44 + i * 34
        rows += (f'<rect x="250" y="{y}" width="230" height="26" rx="6" class="{"f-sel" if sel else "f-box"}"/>'
                 f'<text x="262" y="{y+17}" class="f-mono">{name}</text><text x="468" y="{y+17}" text-anchor="end" class="f-mono">₹{amt}</text>')
        if sel:
            rows += f'<path d="M190,105 C220,105 220,{y+13} 250,{y+13}" class="f-link"/>'
    return f'''<svg class="fig" viewBox="0 0 520 230" role="img" aria-labelledby="ss-t ss-d">
<title id="ss-t">Matching one payment to several invoices</title>
<desc id="ss-d">A payment of 48,200 rupees is matched to three of five open invoices, 12,000, 18,500 and 17,700, which add up exactly.</desc>
<rect x="30" y="80" width="160" height="50" rx="8" class="f-pay"/>
<text x="110" y="101" text-anchor="middle" class="f-small f-inv">payment</text>
<text x="110" y="121" text-anchor="middle" class="f-mono f-inv">₹48,200</text>
{rows}
<text x="365" y="30" text-anchor="middle" class="f-small">open invoices</text>
<text x="110" y="168" text-anchor="middle" class="f-small">difference 0 · 3 invoices</text>
<text x="110" y="186" text-anchor="middle" class="f-small">objective = diff × 1000 + count</text>
</svg>
<p class="fig-cap">Illustration with made-up amounts. The search keeps every amount in integer paise.</p>'''


def fig_pipeline():
    steps = [("Normalize", "accents, abbreviations, digits"), ("Block", "4 lanes: exact anchors, TF-IDF, geography, rare tokens"),
             ("Prune", "a cheap model drops unlikely pairs early"), ("Rerank", "richer features and a cross-encoder"),
             ("Decide", "threshold tuned for F0.5, then resolve conflicts")]
    out = ""
    for i, (a, b) in enumerate(steps):
        y = 34 + i * 50
        out += (f'<rect x="20" y="{y}" width="480" height="38" rx="8" class="{"f-sel" if i == 1 else "f-box"}"/>'
                f'<text x="36" y="{y+24}" class="f-strong">{a}</text>'
                f'<text x="132" y="{y+24}" class="f-small">{b}</text>')
        if i < len(steps) - 1:
            out += f'<path d="M60,{y+38} L60,{y+50}" class="f-arrow"/>'
    return f'''<svg class="fig" viewBox="0 0 520 330" role="img" aria-labelledby="pl-t pl-d">
<title id="pl-t">Entity-resolution pipeline</title>
<desc id="pl-d">Records are normalized, candidates come from four blocking lanes, a cheap model prunes them, richer features and a cross-encoder rerank them, and a threshold tuned for F0.5 plus conflict resolution makes the final links. Underneath is the shared harness: folds, metric, experiment log and submission validator.</desc>
<text x="20" y="20" class="f-small">competition system · 17 country shards on Kaggle</text>
{out}
<rect x="20" y="286" width="480" height="34" rx="8" class="f-band"/>
<text x="260" y="308" text-anchor="middle" class="f-small">shared harness: folds · metric · experiment log · submission validator</text>
</svg>'''


def fig_settlement():
    boxes = [("Buyer returns", "confirms order"), ("Ask Cashfree", "status + amount"), ("One transaction", "paid + 1 sale"), ("Library", "download unlocked")]
    out = ""
    for i, (a, b) in enumerate(boxes):
        x = 12 + i * 127
        cls = "f-sel" if i == 2 else "f-box"
        out += (f'<rect x="{x}" y="50" width="116" height="62" rx="8" class="{cls}"/>'
                f'<text x="{x+58}" y="76" text-anchor="middle" class="f-strong">{a}</text>'
                f'<text x="{x+58}" y="95" text-anchor="middle" class="f-tiny">{b}</text>')
        if i < len(boxes) - 1:
            out += f'<path d="M{x+116},81 L{x+127},81" class="f-arrow"/>'
    return f'''<svg class="fig" viewBox="0 0 520 190" role="img" aria-labelledby="st-t st-d">
<title id="st-t">Settlement flow</title>
<desc id="st-d">The buyer returns and confirms the order, the API checks the order with Cashfree including the exact amount, then one database transaction marks it paid and counts the sale, and the library unlocks the download. A duplicate confirmation finds the order already paid and changes nothing.</desc>
{out}
<path d="M320,150 C320,128 320,124 320,114" class="f-arrow"/>
<text x="320" y="170" text-anchor="middle" class="f-small">a duplicate confirmation finds “paid” and changes nothing</text>
</svg>'''


def fig_dd():
    return '''<svg class="fig" viewBox="0 0 520 220" role="img" aria-labelledby="dd-t dd-d">
<title id="dd-t">Due Diligence architecture</title>
<desc id="dd-d">A Next.js frontend calls Spring Boot controllers secured with JWT. Services aggregate property data from several sources, a risk engine scores six categories, and report and AI assistant features use the same context. PostgreSQL stores the data. Exports pass the same owner-or-admin check as the report.</desc>
<rect x="12" y="84" width="96" height="52" rx="8" class="f-box"/><text x="60" y="114" text-anchor="middle" class="f-strong">Next.js</text>
<path d="M108,110 L126,110" class="f-arrow"/>
<rect x="126" y="24" width="270" height="172" rx="10" class="f-band"/>
<text x="261" y="44" text-anchor="middle" class="f-small">Spring Boot · JWT · owner-or-admin checks</text>
<rect x="140" y="58" width="116" height="40" rx="7" class="f-box"/><text x="198" y="82" text-anchor="middle" class="f-strong">Aggregation</text>
<rect x="266" y="58" width="116" height="40" rx="7" class="f-sel"/><text x="324" y="82" text-anchor="middle" class="f-strong">Risk engine ×6</text>
<rect x="140" y="112" width="116" height="40" rx="7" class="f-box"/><text x="198" y="136" text-anchor="middle" class="f-strong">AI assistant</text>
<rect x="266" y="112" width="116" height="40" rx="7" class="f-box"/><text x="324" y="136" text-anchor="middle" class="f-strong">PDF · Excel</text>
<text x="261" y="178" text-anchor="middle" class="f-tiny">async report generation · in-app + email notification</text>
<path d="M396,110 L414,110" class="f-arrow"/>
<rect x="414" y="84" width="96" height="52" rx="8" class="f-box"/><text x="462" y="114" text-anchor="middle" class="f-strong">PostgreSQL</text>
</svg>'''


FIGURES = {"cashflow": fig_cashflow, "subset": fig_subset, "pipeline": fig_pipeline, "settlement": fig_settlement, "dd": fig_dd}
CASE_FIGURE = {"buy-or-wait": "cashflow", "gumora": "settlement", "settlemate": "subset", "amazon-ml": "pipeline", "due-diligence": "dd"}

# ---------------------------------------------------------------- layout


def schema(extra=None):
    person = {
        "@context": "https://schema.org", "@type": "Person", "@id": BASE + "/#person", "name": P["name"],
        "url": BASE + "/", "sameAs": [P["github"], P["linkedin"], P["leetcode"]],
        "affiliation": {"@type": "CollegeOrUniversity", "name": "BGS College of Engineering and Technology"},
        "knowsAbout": ["Backend development", "Full-stack development", "Java", "Spring Boot", "TypeScript", "Node.js", "Python", "PostgreSQL", "MongoDB", "Applied machine learning"],
    }
    items = [person, {"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "/#website", "name": "Akshaya R", "url": BASE + "/"}]
    if extra:
        items.append(extra)
    return json.dumps(items, ensure_ascii=False).replace("<", "\\u003c")


def shell(title, description, path, body, extra_schema=None, theme_color="#f6f3ec"):
    canonical = BASE + path
    robots = "noindex,follow" if path == "/404.html" else "index,follow"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description, quote=True)}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="{theme_color}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Akshaya R">
<meta property="og:title" content="{E(title, quote=True)}">
<meta property="og:description" content="{E(description, quote=True)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/social.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Akshaya R, software engineer: backend, full-stack and applied ML projects">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title, quote=True)}">
<meta name="twitter:description" content="{E(description, quote=True)}">
<meta name="twitter:image" content="{BASE}/assets/social.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{schema(extra_schema)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
<div class="wrap head-row">
<a class="wordmark" href="/" aria-label="Akshaya R, home">Akshaya R</a>
<nav aria-label="Main">
<a href="/#work">Work</a><a href="/#about">About</a><a href="/#experience">Experience</a><a href="/#contact">Contact</a>
</nav>
</div>
</header>
{body}
<footer class="site-foot">
<div class="wrap foot-row">
<p>Akshaya R · Bengaluru</p>
<p><a href="{P["github"]}">GitHub</a><a href="{P["linkedin"]}">LinkedIn</a><a href="https://github.com/AkshayAlgoX/AkshayAlgoX.github.io">Site source</a></p>
</div>
</footer>
</body>
</html>
'''


def contact_links(primary=True):
    resume = (f'<a class="btn ghost" href="{P["resume_url"]}">Résumé</a>' if P.get("resume_url")
              else '')
    return (f'<a class="btn{" primary" if primary else ""}" href="{P["linkedin"]}">LinkedIn</a>'
            f'<a class="btn ghost" href="{P["github"]}">GitHub</a>{resume}')


def feature_media(p):
    v = p["visual"]
    if v["type"] == "image":
        inset = ""
        if v.get("inset"):
            inset = img(v["inset"], v["inset_alt"], sizes="(min-width: 900px) 18vw, 40vw", cls="inset")
        return f'<div class="shot">{img(v["image"], v["alt"])}</div>{inset}'
    if v["type"] == "figure":
        return f'<div class="panel">{FIGURES[v["figure"]]()}</div>'
    # image + figure
    return (f'<div class="result-shot">{img(v["image"], v["alt"], sizes="(min-width: 900px) 40vw, 90vw")}</div>'
            f'<div class="panel">{FIGURES[v["figure"]]()}</div>')


def homepage():
    a = P["achievement"]
    featured = ""
    for i, p in enumerate(SITE["featured"]):
        badge = f'<p class="badge">{E(p["badge"])}</p>' if p.get("badge") else ""
        status = f'<p class="status">{E(p["status"])}</p>' if p.get("status") else ""
        live = f'<a href="{p["live"]}">Live site</a>' if p.get("live") else ""
        featured += f'''
<article class="feature t-{p["theme"]}{" flip" if i % 2 else ""}" id="{p["slug"]}" aria-labelledby="h-{p["slug"]}">
<div class="feature-media">{feature_media(p)}</div>
<div class="feature-text">
<p class="context">{E(p["context"])}</p>
<h3 id="h-{p["slug"]}"><a href="/projects/{p["slug"]}/">{E(p["title"])}</a></h3>
{badge}
<p class="what">{E(p["what"])}</p>
<p><strong>Why it’s tricky.</strong> {E(p["why"])}</p>
<p><strong>What I did.</strong> {E(p["interesting"])}</p>
<p class="stack">{" · ".join(E(s) for s in p["stack"])}</p>
{status}
<p class="links"><a class="more" href="/projects/{p["slug"]}/">Read the case study</a><a href="https://github.com/AkshayAlgoX/{p["repo"]}">Code</a>{live}</p>
</div>
</article>'''
    more = ""
    for m in SITE["more"]:
        thumb = (img(m["image"], m["alt"], sizes="(min-width: 900px) 30vw, 100vw") if m.get("image")
                 else '<div class="thumb-text" aria-hidden="true"><span>518 deletion requests</span><span>94 evidence files</span><span>0 model calls</span></div>')
        live = f'<a href="{m["live"]}">Live site</a>' if m.get("live") else ""
        more += f'''<article class="card" id="{m.get("id", "")}">
<div class="thumb">{thumb}</div>
<h3>{E(m["title"])}</h3>
<p>{E(m["text"])}</p>
<p class="stack">{E(m["meta"])}</p>
<p class="links"><a href="https://github.com/AkshayAlgoX/{m["repo"]}">Code</a>{live}</p>
</article>'''
    caps = ""
    for c in SITE["capabilities"]:
        seen = ", ".join(f'<a href="{href}">{E(name)}</a>' for name, href in c["seen"])
        caps += f'<li class="cap"><h3>{E(c["title"])}</h3><p>{E(c["text"])}</p><p class="seen">See: {seen}</p></li>'
    exp = ""
    for x in SITE["experience"]:
        pts = "".join(f"<li>{E(t)}</li>" for t in x["points"])
        note = f'<p class="note">{E(x["note"])}</p>' if x.get("note") else ""
        link = f'<p><a class="more" href="{x["link"][1]}">{E(x["link"][0])}</a></p>' if x.get("link") else ""
        exp += f'''<li class="job"><div class="job-head"><h3>{E(x["org"])}</h3><p class="when">{E(x["when"])}</p></div>
<p class="role">{E(x["role"])}</p><ul>{pts}</ul>{note}{link}</li>'''
    about = "".join(f"<p>{E(t)}</p>" for t in SITE["about"])
    resume_line = ("" if P.get("resume_url") else
                   '<p class="small">My résumé is available on request; message me on LinkedIn.</p>')
    body = f'''<main id="main">
<section class="hero wrap" aria-labelledby="name">
<div class="hero-text">
<p class="hello">Hi, I’m</p>
<h1 id="name">Akshaya R</h1>
<p class="lead">{E(P["lead"])}</p>
<p class="intro">{E(P["intro"])}</p>
<div class="cta"><a class="btn primary" href="#work">Explore projects</a>{contact_links(primary=False)}</div>
<a class="win" href="{a["href"]}"><span class="win-value">{E(a["value"])}</span><span class="win-label">{E(a["label"])}</span></a>
</div>
<div class="hero-art" aria-label="Glimpses of two projects">
<figure class="glimpse g1"><div class="chrome" aria-hidden="true"><i></i><i></i><i></i><span>Glucose Twin · patient forecast</span></div>{img("t2d-forecast", "Glucose Twin patient workspace: observed glucose, the physiology twin and a two-hour forecast with uncertainty bands", sizes="(min-width: 900px) 44vw, 92vw", eager=True)}</figure>
<figure class="glimpse g2">{img("dd-landing", "Due Diligence landing page: Property risk, uncovered in seconds", sizes="(min-width: 900px) 24vw, 60vw", eager=True)}</figure>
<p class="art-cap">Real screens: <a href="#glucose-twin">Glucose Twin</a>, <a href="#due-diligence">Due Diligence</a></p>
</div>
</section>

<section id="work" class="work" aria-labelledby="work-title">
<div class="wrap">
<div class="section-head"><h2 id="work-title">Selected work</h2><p>Five projects I’d most like you to look at, two of them competition entries. Each one links to the code and to a longer write-up.</p></div>
{featured}
</div>
</section>

<section id="capabilities" class="capabilities wrap" aria-labelledby="cap-title">
<div class="section-head"><h2 id="cap-title">What I can do</h2><p>Each of these comes from a project you can open and read.</p></div>
<ul class="caps">{caps}</ul>
</section>

<section class="more-projects wrap" aria-labelledby="more-title">
<div class="section-head"><h2 id="more-title">More projects</h2></div>
<div class="cards">{more}</div>
</section>

<section id="about" class="about wrap" aria-labelledby="about-title">
<div class="about-text"><h2 id="about-title">About me</h2>{about}</div>
<div class="about-side"><h3>Technologies used in selected projects</h3><p>{E(SITE["technologies"])}</p></div>
</section>

<section id="experience" class="experience wrap" aria-labelledby="exp-title">
<h2 id="exp-title">Experience</h2>
<ol class="jobs">{exp}
<li class="job"><div class="job-head"><h3>BGS College of Engineering and Technology</h3><p class="when">2023 – 2027 · Bengaluru</p></div><p class="role">B.E. Computer Science and Engineering · CGPA 8.49 / 10</p></li>
</ol>
</section>

<section id="contact" class="contact" aria-labelledby="contact-title">
<div class="wrap contact-row">
<div><h2 id="contact-title">Let’s talk</h2><p>I’m looking for software engineering roles in backend, full-stack and applied ML. LinkedIn is the best way to reach me.</p>{resume_line}</div>
<div class="cta">{contact_links()}<a class="btn ghost" href="{P["leetcode"]}">LeetCode</a></div>
</div>
</section>
</main>'''
    return shell("Akshaya R · Software engineer (backend, full-stack, applied ML)",
                 "Akshaya R is a computer science undergraduate in Bengaluru building backend and full-stack systems: payment settlement, financial reconciliation and ML pipelines. Projects, code and contact.",
                 "/", body)


def case_page(i, p):
    feats = SITE["featured"]
    nxt = feats[(i + 1) % len(feats)]
    glance = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in p["glance"])
    sections = ""
    fig_after = 1 if p["slug"] in ("gumora", "buy-or-wait") else 2
    for n, (head, paras) in enumerate(p["sections"]):
        body = "".join(f"<p>{inline(t)}</p>" for t in paras)
        sections += f'<section aria-labelledby="s{n}"><h2 id="s{n}">{E(head)}</h2>{body}</section>'
        if n == fig_after and p["visual"]["type"] != "figure":
            sections += f'<figure class="case-fig">{FIGURES[CASE_FIGURE[p["slug"]]]()}</figure>'
        if n == fig_after + 1 and p.get("code"):
            c = p["code"]
            note = f'<figcaption>{E(p.get("code_note", ""))}</figcaption>' if p.get("code_note") else ""
            sections += (f'<figure class="code"><div class="code-head"><span>{E(c["label"])}</span>'
                         f'<a href="{source_url(p, c["path"])}">View file</a></div>'
                         f'<pre><code>{E(c["text"])}</code></pre>{note}</figure>')
    if p.get("team"):
        names = ", ".join(f'<a href="https://github.com/{t}">{E(t)}</a>' if t != "DempRepo" else "DempRepo" for t in p["team"])
        sections += (f'<section aria-labelledby="team"><h2 id="team">The team</h2><p>Team 03 built this together: {names}, '
                     f'mentored by <a href="https://github.com/springboardmentor198">springboardmentor198</a>. '
                     f'The <a href="https://github.com/springboardmentor198/team-03">program repository</a> has the shared history.</p></section>')
    srcs = "".join(f'<li><a href="{source_url(p, path)}">{E(label)}</a></li>' for label, path in p["sources"])
    srcs += "".join(f'<li><a href="{url}">{E(label)}</a></li>' for label, url in p.get("extra_links", []))
    status = f'<p class="status">{E(p["status"])}</p>' if p.get("status") else ""
    live = f'<a class="btn ghost" href="{p["live"]}">Live site</a>' if p.get("live") else ""
    v = p["visual"]
    if v["type"] in ("image",):
        hero = f'<div class="case-hero-media">{img(v["image"], v["alt"], sizes="(min-width: 1100px) 1000px, 100vw", eager=True)}</div>'
    elif v["type"] == "image+figure":
        hero = f'<div class="case-hero-media result">{img(v["image"], v["alt"], sizes="(min-width: 1100px) 1000px, 100vw", eager=True)}</div>'
    else:
        hero = f'<figure class="case-hero-fig">{FIGURES[CASE_FIGURE[p["slug"]]]()}</figure>'
    body = f'''<main id="main" class="case t-{p["theme"]}">
<div class="case-top"><div class="wrap">
<p class="crumb"><a href="/#work">{chevron("left")}All projects</a></p>
<p class="context">{E(p["context"])}</p>
<h1>{E(p["title"])}</h1>
<p class="lead">{E(p["what"])}</p>
<div class="cta"><a class="btn primary" href="https://github.com/AkshayAlgoX/{p["repo"]}">View the code</a>{live}</div>
{status}
</div></div>
<div class="wrap">{hero}
<div class="case-grid">
<article class="case-body">{sections}</article>
<aside class="case-side" aria-label="Project details">
<h2 class="side-title">At a glance</h2><dl class="glance">{glance}</dl>
<h2 class="side-title">In the code</h2><ul class="sources">{srcs}</ul>
<p class="pin">Links point to commit <code>{E(p["sha"])}</code>.</p>
</aside>
</div>
<p class="next"><a href="/projects/{nxt["slug"]}/"><span>Next project</span><strong>{E(nxt["title"])}</strong>{chevron()}</a></p>
</div>
</main>'''
    extra = {"@context": "https://schema.org", "@type": "CreativeWork", "name": p["title"], "url": f"{BASE}/projects/{p['slug']}/",
             "author": {"@id": BASE + "/#person"},
             "about": {"@type": "SoftwareSourceCode", "name": p["title"], "codeRepository": f"https://github.com/AkshayAlgoX/{p['repo']}"}}
    return shell(f"{p['title']} · Akshaya R", p["summary"], f"/projects/{p['slug']}/", body, extra)


def inline(text):
    """Escape text; render `code` spans."""
    parts = E(text).split("`")
    return "".join(f"<code>{s}</code>" if k % 2 else s for k, s in enumerate(parts))


def page_404():
    body = '''<main id="main" class="wrap notfound">
<h1>Page not found</h1>
<p>That page doesn’t exist, or it moved.</p>
<p><a class="btn primary" href="/">Go to the homepage</a> <a class="btn ghost" href="/#work">See my projects</a></p>
</main>'''
    return shell("Page not found · Akshaya R", "This page doesn’t exist. Go to Akshaya R’s homepage for projects and contact links.", "/404.html", body)


def main():
    scan_images()
    out = {"index.html": homepage(), "404.html": page_404()}
    for i, p in enumerate(SITE["featured"]):
        out[f"projects/{p['slug']}/index.html"] = case_page(i, p)
    for rel, text in out.items():
        f = ROOT / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    pages = ["/"] + [f"/projects/{p['slug']}/" for p in SITE["featured"]]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"  <url><loc>{BASE}{u}</loc></url>\n" for u in pages) + "</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    dist = ROOT / "dist"
    shutil.rmtree(dist, ignore_errors=True)
    dist.mkdir()
    for rel in ["index.html", "404.html", "sitemap.xml", "robots.txt", ".nojekyll"]:
        shutil.copy2(ROOT / rel, dist / rel)
    shutil.copytree(ROOT / "projects", dist / "projects")
    (dist / "assets").mkdir()
    for f in ["site.css", "favicon.svg", "social.png"]:
        shutil.copy2(ROOT / "assets" / f, dist / "assets" / f)
    shutil.copytree(ROOT / "assets/img", dist / "assets/img")
    print(f"built {len(out)} pages; dist ready")


if __name__ == "__main__":
    main()
