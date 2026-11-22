import json, re, glob, unicodedata, os, sys
base = sys.argv[1]
def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('\x0c','')
    return re.sub(r'[ \t]+\n','\n', s)
def load(prefix, n, ocrpfx, digits):
    pages=[]
    for i in range(1,n+1):
        t = norm(open(f'{base}/{prefix}/p{i}.txt', encoding='utf-8', errors='replace').read())
        ocr=None
        for f in glob.glob(f'{base}/{ocrpfx}_{i}-*.txt'):
            o = norm(open(f).read()).strip()
            if len(re.sub(r'\s','',t))<200 and len(o)>len(re.sub(r'\s','',t)):
                ocr=o
        if ocr: t = (t.strip()+'\n\n[OCR of page image]\n'+ocr).strip()
        # collapse runs of spaces from -layout for readability
        t = re.sub(r' {3,}','   ', t)
        pages.append(t.strip())
    return pages
docs = [
 {"id":"FOI","ref":"FOI/202600522764","title":"Green Data Centre guidance: FOI release — Annex",
  "page_url":"https://www.gov.scot/publications/foi-202600522764/","published":"2 November 2026",
  "pages": load('pages',147,'ocr',3)},
 {"id":"EIR","ref":"EIR/202600522802","title":"Data centre guidance: EIR release — Annex",
  "page_url":"https://www.gov.scot/publications/foi-202600522802/","published":"3 November 2026",
  "pages": load('epages',36,'eocr',2)},
]
# item index: emails by Sent/Subject
items=[]
for d in docs:
    for pi,t in enumerate(d['pages'],1):
        lines=t.split('\n')
        for li,l in enumerate(lines):
            m=re.match(r'\s*(Sent|Date):\s*(.+)',l)
            if m and re.search(r'20\d\d',m.group(2)):
                subj=''
                for l2 in lines[li+1:li+6]:
                    s=re.match(r'\s*Subject:\s*(.+)',l2)
                    if s: subj=s.group(1).strip(); break
                if not subj: continue
                frm=''
                for l0 in lines[max(0,li-2):li]:
                    f=re.match(r'\s*From:\s*(.+)',l0)
                    if f: frm=f.group(1).strip()
                items.append({"doc":d['id'],"page":pi,"date":m.group(2).strip(),"subject":subj,"from":frm})
json.dump({"docs":docs,"items":items}, open(f'{base}/index.json','w'), ensure_ascii=False)
print(len(items), sum(len(d['pages']) for d in docs), os.path.getsize(f'{base}/index.json'))
for it in items[:8]: print(it)
# meetings
for d in docs:
    for pi,t in enumerate(d['pages'],1):
        if 'Meeting Title' in t:
            m=re.search(r'Meeting Title\s+(.+)',t); dt=re.search(r'Date and Time\s+(.+)',t)
            if m and dt: items.append({"doc":d['id'],"page":pi,"date":dt.group(1).strip(),"subject":"MINUTES: "+m.group(1).strip(),"from":""})
from datetime import datetime
def key(it):
    s=re.sub(r'(\d+)(st|nd|rd|th)',r'\1',it['date']).replace(',','')
    for fmt in ('%d %B %Y %H:%M','%d %B %Y','%A %d %B %Y %H:%M','%A %B %d %Y %I:%M %p'):
        try: return datetime.strptime(s.strip(),fmt).isoformat()
        except: pass
    m=re.search(r'(\d{1,2}) (\w+) (20\d\d)',s)
    if m:
        try: return datetime.strptime(m.group(0),'%d %B %Y').isoformat()
        except: pass
    return ''
for it in items: it['iso']=key(it)
json.dump({"docs":docs,"items":items}, open(f'{base}/index.json','w'), ensure_ascii=False)
print('items',len(items),'undated',sum(1 for i in items if not i['iso']))
