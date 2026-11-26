"""Link maintenance.
  python3 tools/redlinks.py targets          -> write tools/link_targets.txt (all [[links]] that are not our own articles)
  python3 tools/redlinks.py unlink FILE      -> FILE lists titles missing on he.wikipedia (one per line); unlink them in wiki/*.wiki
  python3 tools/redlinks.py new [FILE.wiki]  -> print targets (of FILE, or of all articles) not yet in tools/known_ok.txt, plus a
                                                he.wikipedia API URL to check them (50 titles per URL)
  python3 tools/redlinks.py ok FILE          -> add the titles in FILE (checked and found to exist) to tools/known_ok.txt
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
elif sys.argv[1] in ('new', 'ok'):
    import urllib.parse
    known = set()
    if os.path.exists('tools/known_ok.txt'):
        known = {l.strip() for l in open('tools/known_ok.txt', encoding='utf-8') if l.strip()}
    if sys.argv[1] == 'ok':
        known |= {l.strip() for l in open(sys.argv[2], encoding='utf-8') if l.strip()}
        open('tools/known_ok.txt', 'w', encoding='utf-8').write('\n'.join(sorted(known)) + '\n')
        print(len(known), 'known')
        sys.exit()
    files = sys.argv[2:] or glob.glob('wiki/*.wiki')
    ts = set()
    for f in files:
        for m in LINK.finditer(open(f, encoding='utf-8').read()):
            t = m.group(1).strip()
            if t and not SKIP.match(t) and t not in ours and t not in known:
                ts.add(t)
    ts = sorted(ts)
    for t in ts:
        print(t)
    for i in range(0, len(ts), 50):
        print('https://he.wikipedia.org/w/api.php?action=query&format=json&redirects=1&titles=' + urllib.parse.quote('|'.join(ts[i:i + 50])))
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
