#!/usr/bin/env python3
"""Link the first plain mention of a title (or given surface forms) in each article.

usage: relink.py TITLE [FORM ...]
Skips the article itself, articles that already link to TITLE, and text inside
<math>, templates, existing links, headings and the reading-list div.
"""
import re, sys, glob, os
title = sys.argv[1]
forms = sys.argv[2:] or [title]
changed = []
for p in sorted(glob.glob('wiki/*.wiki')):
    if os.path.basename(p)[:-5] == title:
        continue
    s = open(p, encoding='utf-8').read()
    if '[[' + title + ']]' in s or '[[' + title + '|' in s:
        continue
    # protected spans
    prot = [m.span() for m in re.finditer(r'<math.*?</math>|\{\{.*?\}\}|\[\[.*?\]\]|^=[^\n]*=$|<div dir="ltr">.*?</div>', s, re.S | re.M)]
    best = None
    for f in forms:
        for m in re.finditer(r'(?<![\w\[])(?:[והבלמשכ]{0,2})(' + re.escape(f) + r')(?![\w])', s):
            if any(a <= m.start(1) < b for a, b in prot):
                continue
            if best is None or m.start() < best[0]:
                best = (m.start(1), m.end(1), f)
            break
    if best:
        a, b, f = best
        link = '[[' + title + ']]' if f == title else '[[' + title + '|' + f + ']]'
        s = s[:a] + link + s[b:]
        open(p, 'w', encoding='utf-8').write(s)
        changed.append(os.path.basename(p))
print('relinked', len(changed), changed)
