#!/usr/bin/env python3
"""Give orphan articles (no incoming links from other articles) an incoming link.

For each orphan O, pick the local article P that O links to and that shares the most
categories with O (ties: P with fewer outgoing links), and add "* [[O]]" to P's
"ראו גם" section (created if missing, before the reading list / footnotes / categories).
usage: python3 tools/adopt.py [--dry]
"""
import glob, os, re, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
dry = '--dry' in sys.argv
LINK = re.compile(r'\[\[([^\]|#]+)')
CAT = re.compile(r'\[\[קטגוריה:([^\]|]+)')
txt = {os.path.basename(f)[:-5]: open(f, encoding='utf-8').read() for f in glob.glob('wiki/*.wiki')}
ours = set(txt)
out = {t: {m.group(1).strip() for m in LINK.finditer(s)} & ours - {t} for t, s in txt.items()}
cats = {t: set(CAT.findall(s)) for t, s in txt.items()}
inc = {t: 0 for t in ours}
for t, o in out.items():
    for x in o:
        inc[x] += 1
orph = sorted(t for t in ours if inc[t] == 0)
END = re.compile(r'^(== *(לקריאה נוספת|קישורים חיצוניים|הערות שוליים) *==|\[\[קטגוריה:)', re.M)
done = []
for o in orph:
    cands = [p for p in out[o] if p != o]
    if cands:
        p = max(cands, key=lambda p: (len(cats[o] & cats[p]), -len(out[p])))
    else:
        # no outgoing local links: fall back to the article sharing most categories / title words
        words = set(o.split())
        p = max((p for p in ours if p != o), key=lambda p: (len(cats[o] & cats[p]), len(words & set(p.split())), -len(out[p])))
        if not cats[o] & cats[p]:
            continue
    s = txt[p]
    if '[[' + o + ']]' in s or '[[' + o + '|' in s:
        continue
    m = re.search(r'^== *ראו גם *==\n((?:\*.*\n)*)', s, re.M)
    if m:
        s = s[:m.end()] + '* [[' + o + ']]\n' + s[m.end():]
    else:
        e = END.search(s)
        pos = e.start() if e else len(s)
        s = s[:pos] + '== ראו גם ==\n* [[' + o + ']]\n\n' + s[pos:]
    txt[p] = s
    done.append((o, p))
    if not dry:
        open('wiki/' + p + '.wiki', 'w', encoding='utf-8').write(s)
for o, p in done:
    print(o, '<-', p)
print(len(orph), 'orphans;', len(done), 'adopted')
