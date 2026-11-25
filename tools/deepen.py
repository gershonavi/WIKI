import sys, glob, urllib.parse
"""usage: deepen.py LESSON_PREFIX title [title...] -- append links to the lesson's **להעמקה:** line"""
pre, titles = sys.argv[1], sys.argv[2:]
f = glob.glob(f'course/{pre}-*.md')[0]
L = open(f).read().split('\n')
i = max(k for k, l in enumerate(L) if l.startswith('**להעמקה:**'))
for t in titles:
    if f'[{t}]' not in L[i]:
        L[i] += f' · [{t}](../pages/{t.replace(" ", "%20")}.md)'
open(f, 'w').write('\n'.join(L))
print(f, 'ok')
