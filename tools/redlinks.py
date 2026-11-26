"""Link maintenance.
  python3 tools/redlinks.py targets          -> write tools/link_targets.txt (all [[links]] that are not our own articles)
  python3 tools/redlinks.py unlink FILE      -> FILE lists titles missing on he.wikipedia (one per line); unlink them in wiki/*.wiki
The missing-title check itself is done against the he.wikipedia API (see tools/links.py for the JS approach)."""
import re, os, sys, glob
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ours = {os.path.basename(f)[:-5] for f in glob.glob('wiki/*.wiki')}
SKIP = re.compile(r'(קטגוריה|קובץ|File|Category|Image|תמונה|en|w|ויקיפדיה|wikt):', re.I)
LINK = re.compile(r'\[\[([^\]|#]+)(#[^\]|]*)?(?:\|([^\]]+))?\]\]')

if sys.argv[1] == 'targets':
    ts = set()
    for f in glob.glob('wiki/*.wiki'):
        for m in LINK.finditer(open(f, encoding='utf-8').read()):
            t = m.group(1).strip()
            if t and not SKIP.match(t) and t not in ours:
                ts.add(t)
    open('tools/link_targets.txt', 'w', encoding='utf-8').write('\n'.join(sorted(ts)) + '\n')
    print(len(ts), 'targets')
elif sys.argv[1] == 'unlink':
    missing = {l.strip() for l in open(sys.argv[2], encoding='utf-8') if l.strip()} - ours
    n = 0
    for f in glob.glob('wiki/*.wiki'):
        s = open(f, encoding='utf-8').read()
        def rep(m):
            global n
            t = m.group(1).strip()
            if t in missing:
                n += 1
                return m.group(3) or t
            return m.group(0)
        s2 = LINK.sub(rep, s)
        if s2 != s:
            open(f, 'w', encoding='utf-8').write(s2)
    print('unlinked', n)
