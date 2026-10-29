#!/usr/bin/env python3
"""Dependency-free checks for the published artifact, links and claim guardrails."""
import json,pathlib,re,sys,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=pathlib.Path(__file__).resolve().parents[1];DIST=ROOT/'dist';BASE='https://akshayalgox.github.io'
class Document(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.ids=[];self.h1=0;self.jsons=[];self.in_json=False;self.buf='';self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a));self.h1+=tag=='h1'
  if 'id'in a:self.ids.append(a['id'])
  if tag=='script' and a.get('type')=='application/ld+json':self.in_json=True;self.buf=''
 def handle_data(self,text):
  if self.in_json:self.buf+=text
 def handle_endtag(self,tag):
  if tag=='script' and self.in_json:self.jsons.append(json.loads(self.buf));self.in_json=False
errors=[];checks=0

def check(condition,label):
 global checks
 checks+=1
 if not condition:errors.append(label)
files=sorted(DIST.rglob('*.html'));docs={p:Document(p.read_text()) for p in files}
for p,d in docs.items():
 label=str(p.relative_to(DIST));tags=d.tags
 check(d.h1==1,label+': exactly one h1');check(len(d.ids)==len(set(d.ids)),label+': unique IDs')
 check(any(t=='main' for t,a in tags),label+': main landmark')
 check(any(t=='html' and a.get('lang')=='en' for t,a in tags),label+': language')
 check(any(t=='a' and a.get('href')=='#main' for t,a in tags),label+': skip link')
 check(any(t=='title' for t,a in tags),label+': title')
 for attr,name in [('name','description'),('property','og:title'),('property','og:image'),('name','twitter:card')]:
  check(any(t=='meta' and a.get(attr)==name and a.get('content') for t,a in tags),label+': '+name)
 expected=BASE+('/' if label=='index.html' else '/'+label.removesuffix('index.html'))
 check(any(t=='link' and a.get('rel')=='canonical' and a.get('href')==expected for t,a in tags),label+': canonical')
 check(bool(d.jsons),label+': valid JSON-LD')
 check(all(a.get('type')=='application/ld+json' for t,a in tags if t=='script'),label+': no executable scripts')
 check(not any(t in ['iframe','form'] for t,a in tags),label+': no third-party embeds or data collection')
 text=p.read_text()
 check(not re.search(r'Intent2Data|Tech_Spin|ai-finance|github.com/AkshayAlgoX/hive|498\+|98\.1%|1,246|six-member|OR-Tools N:M|runs OR-Tools|powered by OR-Tools|99%\+? uptime|90% faster|cutting seller onboarding',text,re.I),label+': retired/stale/unsupported claims absent')
 for t,a in tags:
  if t=='img':
   check(bool(a.get('alt','').strip()),label+': image alt text '+a.get('src',''))
   check(a.get('width','').isdigit() and a.get('height','').isdigit(),label+': image dimensions '+a.get('src',''))
 check(not re.search(r'(?i)(?:gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}|BEGIN (?:RSA |EC )?PRIVATE KEY|mailto:|tel:)',text),label+': no credential/private contact patterns')
 for t,a in tags:
  for attr in ['href','src']:
   if attr not in a:continue
   u=urlsplit(a[attr])
   check(u.scheme in ('','https','http'),label+': safe link protocol '+a[attr])
   if u.scheme or u.netloc:continue
   dest=DIST/u.path.lstrip('/') if u.path.startswith('/') else p.parent/u.path
   if not u.path:dest=p
   if dest.is_dir():dest=dest/'index.html'
   check(dest.exists(),label+': target exists '+a[attr])
   if u.fragment and dest in docs:check(unquote(u.fragment) in docs[dest].ids,label+': fragment exists '+a[attr])
site=json.loads((ROOT/'content/site.json').read_text())
for p in site['featured']:
 check(len(p['sections'])>=5,p['slug']+': case study has at least five sections')
 check(all(len(s)==2 and s[1] for s in p['sections']),p['slug']+': valid sections')
 check(len(p['sources'])>=4,p['slug']+': links into the code')
 check(all(p.get(k) for k in ['what','why','interesting','summary']),p['slug']+': homepage summary complete')
 for label,path in p['sources']+([[p['code']['label'],p['code']['path']]] if p.get('code') else []):
  target=ROOT.parent/p['repo']/path.split('#')[0]
  # Source clones are optional in CI; local review checks them when available.
  if (ROOT.parent/p['repo']).exists():check(target.exists(),p['slug']+': pinned source path '+path)
check((DIST/'.nojekyll').exists(),'GitHub Pages static marker')
check((DIST/'assets/social.png').read_bytes()[:8]==b'\x89PNG\r\n\x1a\n','social preview is PNG')
site=ET.parse(DIST/'sitemap.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[e.text for e in site.findall('s:url/s:loc',ns)];check(len(urls)==6,'sitemap has all six content pages');check(all(x.startswith(BASE+'/') for x in urls),'sitemap canonical domain')
check('Sitemap: '+BASE+'/sitemap.xml' in (DIST/'robots.txt').read_text(),'robots points to sitemap')
public_size=sum(p.stat().st_size for p in DIST.rglob('*') if p.is_file())
check(public_size<600000,'complete static artifact below 600 KB')
report={'checks':checks,'failures':errors,'pages':len(files),'public_bytes':public_size}
print(json.dumps(report,indent=2));sys.exit(bool(errors))
