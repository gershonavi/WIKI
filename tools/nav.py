"""Rewrite the previous/next navigation line of every main-course lesson from course/units.tsv order."""
import os, re
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
rows = []
for r in open('course/units.tsv', encoding='utf-8').read().splitlines():
    p = r.split('\t')
    if r.startswith('#') or len(p) < 3 or not os.path.exists('course/' + p[2]):
        continue
    label = (f'שיעור כלים {p[0]}' if p[0].startswith('כ') else f'שיעור {p[0]}') + ': ' + p[1]
    rows.append((p[2], label))
changed = 0
for i, (f, _) in enumerate(rows):
    parts = []
    if i > 0:
        parts.append(f'**השיעור הקודם:** [{rows[i-1][1]}]({rows[i-1][0]})')
    if i + 1 < len(rows):
        parts.append(f'**השיעור הבא:** [{rows[i+1][1]}]({rows[i+1][0]})')
    else:
        parts.append('**חזרה ל:** [תוכן הקורס](../COURSE.md)')
    line = ' · '.join(parts)
    path = 'course/' + f
    L = open(path, encoding='utf-8').read().split('\n')
    idx = [k for k, x in enumerate(L) if x.startswith('**השיעור הקודם:**') or x.startswith('**השיעור הבא:**')]
    if not idx:
        print('no nav line in', f); continue
    if L[idx[-1]] != line:
        L[idx[-1]] = line; changed += 1
        open(path, 'w', encoding='utf-8').write('\n'.join(L))
print('nav lines updated:', changed)
