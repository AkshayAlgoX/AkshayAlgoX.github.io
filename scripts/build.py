#!/usr/bin/env python3
"""Generate committed, crawlable HTML and an allowlisted GitHub Pages preview."""
import html,json,pathlib,shutil
from urllib.parse import quote
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE='https://akshayalgox.github.io'
DATA=json.loads((ROOT/'content/projects.json').read_text())
E=html.escape

def source(p,path):
    clean,sep,frag=path.partition('#')
    kind='tree' if clean in ['src','tests'] else 'blob'
    return f'https://github.com/AkshayAlgoX/{p["repo"]}/{kind}/{p["sha"]}/{quote(clean,safe="/")}' + ('#'+frag if sep else '')

def shell(title,description,path,body,case=None):
    canonical=BASE+path
    schema=[{'@context':'https://schema.org','@type':'Person','@id':BASE+'/#person','name':'Akshaya R','url':BASE+'/','sameAs':['https://github.com/AkshayAlgoX','https://www.linkedin.com/in/akshaya-r-a381873a4/']},{'@context':'https://schema.org','@type':'WebSite','@id':BASE+'/#website','name':'Akshaya R — Engineering Portfolio','url':BASE+'/'}]
    if case: schema.append({'@context':'https://schema.org','@type':'CreativeWork','name':case['title']+' — Engineering Case Study','url':canonical,'about':{'@type':'SoftwareSourceCode','name':case['title'],'codeRepository':'https://github.com/AkshayAlgoX/'+case['repo']}})
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(description,quote=True)}">
<meta name="color-scheme" content="light dark"><meta name="theme-color" content="#a53b22">
<link rel="canonical" href="{canonical}"><meta name="robots" content="{'noindex,follow' if path=='/404.html' else 'index,follow'}">
<meta property="og:type" content="website"><meta property="og:locale" content="en_US">
<meta property="og:title" content="{E(title,quote=True)}"><meta property="og:description" content="{E(description,quote=True)}"><meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/social.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Akshaya R. Software engineering, with the evidence attached.">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title,quote=True)}"><meta name="twitter:description" content="{E(description,quote=True)}"><meta name="twitter:image" content="{BASE}/assets/social.png"><meta name="twitter:image:alt" content="Akshaya R. Software engineering, with the evidence attached.">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')}</script>
</head><body><a class="skip" href="#main">Skip to content</a>
<header class="wrap masthead"><a class="brand" href="/"><span class="monogram" aria-hidden="true">a</span> Akshaya R<span class="folio" aria-hidden="true"> / Engineering</span></a>
<nav class="nav" aria-label="Main navigation"><a href="/#work">Selected work</a><a href="/#about">About</a><a href="/#contact">Contact</a><a href="https://github.com/AkshayAlgoX">GitHub <span aria-hidden="true">↗</span></a></nav></header>
{body}
<footer class="wrap footer"><span>© 2026 Akshaya R · Built with HTML, CSS &amp; evidence.</span><span><a href="https://github.com/AkshayAlgoX/AkshayAlgoX.github.io">Site source ↗</a><a href="/#contact">Professional profiles ↗</a></span></footer></body></html>'''

def flow(p):
    return '<div class="flow">'+''.join(f'<div class="flow-row"><span class="number">{E(n)}</span><div><strong>{E(t)}</strong><small>{E(d)}</small></div></div>' for n,t,d in p['flow'])+'</div>'

def link(p,label='Read case study'):
    return f'<a class="text-link" href="/projects/{p["slug"]}/">{label} <span aria-hidden="true">↗</span></a>'

def homepage():
    p=DATA[0]
    cards=''
    for p2 in DATA[1:]:
        cards+=f'''<article class="project-card"><span class="eyebrow">{E(p2['kicker'])}</span><h3 class="project-title">{E(p2['title'])}</h3><span class="tag">{E(p2['category'])}</span><p>{E(p2['summary'])}</p><div class="actions">{link(p2)}<a class="text-link" href="https://github.com/AkshayAlgoX/{p2['repo']}">Source ↗</a></div><div class="status">{E(p2['status'])}</div></article>'''
    body=f'''<main id="main" class="wrap">
<section class="hero" aria-labelledby="intro"><div class="hero-grid"><div><div class="eyebrow">Akshaya R / Software engineering &amp; applied ML</div><h1 id="intro">Systems that decide.<br><em>Evidence you<br>can inspect.</em></h1><p class="intro">I build full-stack applications and deterministic decision systems, with a focus on exact accounting, reliability and practical ML.</p><div class="actions"><a class="button" href="#work">Explore selected work <span aria-hidden="true">↓</span></a><a class="text-link" href="https://github.com/AkshayAlgoX">View GitHub ↗</a></div></div>
<aside class="system-note" aria-label="Engineering approach"><div class="label"><span>Engineering note / 001</span><span aria-hidden="true">↗</span></div><h2>A decision is only as useful<br>as the reasoning behind it.</h2><div class="decision-row"><b>01</b><span>Constrain the inputs</span><span>validate</span></div><div class="decision-row"><b>02</b><span>Keep the core deterministic</span><span>compute</span></div><div class="decision-row"><b>03</b><span>Test the failure paths</span><span>challenge</span></div><div class="decision-row"><b>04</b><span>Make the result inspectable</span><span>explain</span></div><p class="note-end">A recurring thread across my work:<br>AI can assist. Critical logic needs a contract.</p></aside></div>
<div class="hero-foot"><div class="result-line"><strong>#85</strong><p><b>HackerRank Orchestrate · September 2026</b><br>Individual global rank of 3,062 · score 68.2/100<br><a href="{source(p,'docs/assets/hackerrank_orchestrate_result_banner.png')}">View recorded result ↗</a></p></div><div class="availability"><span class="dot" aria-hidden="true"></span><span>CSE undergraduate · expected graduation 2027<br>Interested in software, full-stack, backend &amp; applied ML roles</span></div></div></section>
<section id="work" class="section" aria-labelledby="selected"><div class="section-head"><div><span class="eyebrow">Selected engineering work / 01–05</span><h2 id="selected">The work, and how it holds up.</h2></div><p>Five case studies. Implementation decisions, test evidence and the limits that matter.</p></div>
<article class="featured"><div><span class="eyebrow">{E(p['kicker'])}</span><h3 class="project-title">{E(p['title'])}</h3><span class="tag">{E(p['category'])}</span><p>{E(p['summary'])} Daily cash-flow constraints shape every recommendation.</p><div class="actions">{link(p)}<a class="text-link" href="https://github.com/AkshayAlgoX/{p['repo']}">Source ↗</a></div></div>{flow(p)}</article><div class="project-grid">{cards}</div></section>
<section class="section" aria-labelledby="more"><div class="section-head"><div><span class="eyebrow">Further explorations</span><h2 id="more">Beyond the featured work.</h2></div><p>Research tooling, market data and evidence-driven audit workflows.</p></div><div class="index-list">
<a class="index-row" href="https://github.com/AkshayAlgoX/T2D-Glucose-Digital-Twin"><span class="number">06</span><h3>Glucose Twin</h3><p>Team research prototype: physiology-informed UKF + learned forecasts. Synthetic demo; no clinical validation. Host returned 503 on 29 Oct 2026.</p><span aria-hidden="true">↗</span></a>
<a class="index-row" href="https://github.com/AkshayAlgoX/Coinpulse"><span class="number">07</span><h3>Coinpulse</h3><p>Next.js market-data dashboard. Server-side CoinGecko access with validated operations.</p><span aria-hidden="true">↗</span></a>
<a class="index-row" href="https://github.com/AkshayAlgoX/orchestrate-october26-work"><span class="number">08</span><h3>Ghost Data Still Exists</h3><p>October Orchestrate deletion-audit workflow: trace remaining data through supplied evidence. No competition result claimed.</p><span aria-hidden="true">↗</span></a></div></section>
<section id="about" class="section" aria-labelledby="about-title"><div class="about-grid"><div><span class="eyebrow">About / Approach</span><h2 id="about-title">Engineering across<br>the boundaries.</h2></div><div class="about-copy"><p>My work sits where application code meets money, data and external services. I’m interested in the parts that demand careful reasoning: a payment callback arriving twice, a solver reaching its limit, or an evaluation that cannot be reproduced from public data.</p><p>I’m a computer science engineering undergraduate at BGS College of Engineering and Technology, with expected graduation in 2027.</p><div class="experience"><h3>Veanka Innosol Pvt. Ltd. / Software Engineer Intern</h3><p>React Native migration and mobile application work. Role supported by my current resume; employer project source remains private.</p><h3>Infosys Springboard / Team 03 project</h3><p>Repository-documented team lead for the due-diligence project, with contributions to backend architecture, authentication and risk scoring. <a href="/projects/due-diligence/">Read contribution context ↗</a></p></div></div></div></section>
<section id="contact" class="contact" aria-labelledby="contact-title"><div><span class="eyebrow">Continue the conversation</span><h2 id="contact-title">Let’s talk about the engineering.</h2><p>For opportunities or a closer look at my work, connect through LinkedIn.</p></div><div class="actions"><a class="button" href="https://www.linkedin.com/in/akshaya-r-a381873a4/">Connect on LinkedIn ↗</a><a class="text-link" href="https://leetcode.com/u/rakshay5764/">LeetCode ↗</a></div></section>
</main>'''
    return shell('Akshaya R — Software Engineering & Applied ML','Full-stack applications and deterministic decision systems by Akshaya R. Explore source-backed case studies in payments, reconciliation and applied ML.','/',body)

def casepage(p,i):
    sections=''
    for j,(title,text) in enumerate(p['sections']):
        sections+=f'<section id="section-{j+1}" aria-labelledby="heading-{j+1}"><h2 id="heading-{j+1}">{E(title)}</h2><p>{E(text)}</p></section>'
    sources=''.join(f'<li><a href="{source(p,path)}">{E(label)}<span aria-hidden="true">↗</span></a></li>' for label,path in p['sources'])
    if p['slug']=='amazon-ml': sources+='<li><a href="https://github.com/AkshayAlgoX/amlc26-harness/blob/91f8d30cd1789ffe8d0418aa25c1cd086ae93667/src/er/metric.py">Specialized ER metric · separate competition branch <span aria-hidden="true">↗</span></a></li>'
    credit=''
    if p['slug']=='due-diligence':
        credit='<aside class="team-credit" aria-label="Team credit"><p>Shared Team 03 delivery. The repository credits MelvinBritto, Bhavana-Bhat-528, tanishaalone30 (commits as tanishaalone-lab), SubashS0411, DempRepo and <a href="https://github.com/NalamothuLokesh">NalamothuLokesh</a>, with mentorship from <a href="https://github.com/springboardmentor198/team-03">springboardmentor198</a>. This contributor list is not a verified official membership count.</p></aside>'
    nxt=DATA[(i+1)%len(DATA)]
    body=f'''<main id="main" class="wrap"><header class="case-hero"><a class="back" href="/#work">← Selected engineering work</a><div class="eyebrow">{E(p['kicker'])}</div><h1>{E(p['title'])}</h1><p class="case-deck">{E(p['summary'])}</p><span class="tag">{E(p['category'])}</span><div class="actions"><a class="button" href="https://github.com/AkshayAlgoX/{p['repo']}">Explore repository ↗</a><a class="text-link" href="#evidence">Inspect the evidence ↓</a></div><dl class="case-facts"><div><dt>Role &amp; attribution</dt><dd>{E(p['role'])}</dd></div><div><dt>Evaluation / availability · 29 Oct 2026</dt><dd>{E(p['status'])}</dd></div><div><dt>{E(p['result_label'])}</dt><dd>{E(p['result'])}{' · score '+E(p['score']) if p.get('score') else ''}</dd></div><div><dt>Evidence scope</dt><dd>Current default-branch source; recorded project tests are not new portfolio test runs.</dd></div></dl></header>
<div class="case-layout"><nav class="contents" aria-label="Case study contents"><span class="label">Inside the case study</span><ol>{''.join(f'<li><a href="#section-{j+1}">{E(t)}</a></li>' for j,(t,_) in enumerate(p['sections']))}<li><a href="#evidence">Source &amp; test evidence</a></li></ol></nav><article class="prose" aria-label="{E(p['title'])} technical case study"><figure class="architecture"><figcaption class="label">Architecture / simplified data flow</figcaption>{flow(p)}</figure>{sections}{credit}<section id="evidence" aria-labelledby="evidence-title"><h2 id="evidence-title">Source &amp; test evidence</h2><p>Implementation and verification links pinned to the reviewed revision, so the case study remains traceable as the project evolves.</p><ul class="source-list">{sources}</ul><p class="source-note">Reviewed 29 October 2026 · revision {p['sha']}</p></section></article></div><div class="next-work"><a href="/#work">← All selected work</a>{link(nxt,'Next: '+E(nxt['title']))}</div><section class="contact"><div><span class="eyebrow">A closer look</span><h2>Discuss the decisions behind the code.</h2></div><a class="button" href="https://www.linkedin.com/in/akshaya-r-a381873a4/">Connect on LinkedIn ↗</a></section></main>'''
    return shell(p['title']+' — Case Study | Akshaya R',p['summary'],'/projects/'+p['slug']+'/',body,p)

(ROOT/'index.html').write_text(homepage())
for i,p in enumerate(DATA):
    out=ROOT/'projects'/p['slug'];out.mkdir(exist_ok=True,parents=True);(out/'index.html').write_text(casepage(p,i))
(ROOT/'404.html').write_text(shell('Page not found — Akshaya R','Find selected engineering work and project case studies.','/404.html','<main id="main" class="wrap error-page"><span class="eyebrow">404 / Page not found</span><h1>A missing link.</h1><p>The work is still here. Head back to the project index.</p><a class="button" href="/#work">View selected work</a></main>'))
paths=['/']+['/projects/'+p['slug']+'/' for p in DATA]
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+BASE+p+'</loc></url>' for p in paths)+'</urlset>\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
(ROOT/'.nojekyll').touch()
dist=ROOT/'dist'
if dist.exists():shutil.rmtree(dist)
dist.mkdir()
for name in ['index.html','404.html','robots.txt','sitemap.xml','.nojekyll','assets','projects']:
    p=ROOT/name
    if p.is_dir():shutil.copytree(p,dist/name)
    else:shutil.copy2(p,dist/name)
print(f'Built {len(paths)} static content pages + 404. No runtime JavaScript or dependencies.')
