#!/usr/bin/env python3
"""Build a static website (for GitHub Pages) from the Markdown in this repository.

Usage: python3 site.py OUTPUT_DIR
Needs pandoc. Run build.py first. The site mirrors the repository layout:
README.md -> index.html, COURSE.md -> COURSE.html, pages/X.md -> pages/X.html, course/X.md -> course/X.html.
It also writes sitemap.xml and robots.txt, so search engines can find every page.
Files in site-static/ (for example a Google Search Console verification file) are copied as they are.
"""
import html, os, re, shutil, subprocess, sys, urllib.parse
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://gershonavi.github.io/WIKI/'
REPO = 'https://github.com/gershonavi/WIKI'

CSS = """
body{font-family:system-ui,-apple-system,"Segoe UI",Arial,sans-serif;line-height:1.7;margin:0;color:#1f2328;background:#fff}
header{background:#f6f8fa;border-bottom:1px solid #d0d7de;padding:.6em 1.2em}
header a{margin-left:1.2em;font-weight:600;color:#0969da;text-decoration:none}
main{max-width:52em;margin:0 auto;padding:1em 1.2em 3em}
a{color:#0969da}
img{max-width:100%;height:auto;display:block;margin:1em auto}
pre,code{direction:ltr;font-family:ui-monospace,Consolas,monospace}
pre{background:#f6f8fa;padding:.8em;overflow-x:auto}
table{border-collapse:collapse;margin:1em 0}
th,td{border:1px solid #d0d7de;padding:.3em .7em}
blockquote{border-right:.25em solid #d0d7de;margin:0;padding:0 1em;color:#59636e}
details{background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:.4em .9em;margin:.8em 0}
summary{cursor:pointer;font-weight:600}
mjx-container[display="true"]{direction:ltr;overflow-x:auto;overflow-y:hidden}
footer{border-top:1px solid #d0d7de;color:#59636e;font-size:.9em;padding:1em 1.2em;text-align:center}
"""

MATHJAX = """<script>window.MathJax={tex:{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>"""


def sources():
    out = [('README.md', 'index.html')]
    for f in ['COURSE.md', 'PROOFS.md', 'CATEGORIES.md', 'LICENSE-CONTENT.md']:
        if os.path.exists(os.path.join(ROOT, f)):
            out.append((f, f[:-3] + '.html'))
    for d in ['pages', 'course', 'categories']:
        for f in sorted(os.listdir(os.path.join(ROOT, d))):
            if f.endswith('.md'):
                out.append((f'{d}/{f}', f'{d}/{f[:-3]}.html'))
    return out


def fix_math(md):
    """GitHub math syntax -> plain TeX delimiters that pandoc passes through to MathJax."""
    md = re.sub(r'^([ ]*)```math\n(.*?)\n[ ]*```', lambda m: m.group(1) + '$$\n' + m.group(2).strip() + '\n' + m.group(1) + '$$', md, flags=re.S | re.M)
    md = re.sub(r'\$`(.+?)`\$', lambda m: '$' + m.group(1).strip() + '$', md)
    return md


def fix_links(md, src):
    def rel(m):
        target = m.group(2)
        if re.match(r'[a-z]+:', target) or target.startswith('#'):
            return m.group(0)
        path, _, frag = target.partition('#')
        if path == 'LICENSE':
            return f'{m.group(1)}({REPO}/blob/main/LICENSE)'
        if path.startswith('../wiki/') or path.startswith('wiki/'):
            return f'{m.group(1)}({REPO}/blob/main/wiki/{path.split("wiki/", 1)[1]})'
        if path.endswith('.md'):
            path = path[:-3] + '.html'
            if os.path.basename(path) == 'README.html':
                path = path[:-11] + 'index.html'
        return f'{m.group(1)}({path}{"#" + frag if frag else ""})'
    return re.sub(r'(\]\s?)\(([^)\s]+)\)', rel, md)


def title_and_description(md):
    m = re.search(r'^# (.+)$', md, flags=re.M)
    title = m.group(1).strip() if m else 'תורת המספרים בעברית'
    body = re.sub(r'^#.*$', '', md, flags=re.M)
    for para in re.split(r'\n\s*\n', body):
        t = para.strip()
        if not t or t.startswith(('!', '<', '|', '```', '$$', '---', '*', '>')):
            continue
        t = re.sub(r'\$`?([^$`]*)`?\$', r'\1', t)
        t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
        t = re.sub(r"[*_`]|'''|''", '', t)
        t = ' '.join(t.split())
        if len(t) > 40:
            return title, (t[:155] + '…') if len(t) > 160 else t
    return title, title


def render(md):
    r = subprocess.run(['pandoc', '-f', 'gfm+tex_math_dollars+footnotes', '-t', 'html5', '--mathjax',
                        '--wrap=none'], input=md, capture_output=True, text=True, check=True)
    return r.stdout


def page(title, desc, body, url, depth):
    up = '../' * depth
    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} – תורת המספרים בעברית</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<style>{CSS}</style>
{MATHJAX}
</head>
<body>
<header><a href="{up}index.html">דף הבית</a><a href="{up}COURSE.html">הקורס</a><a href="{up}PROOFS.html">שיטות הוכחה</a><a href="{REPO}">GitHub</a></header>
<main>
{body}
</main>
<footer>התוכן מתורגם מוויקיפדיה האנגלית ומופץ ברישיון <a href="{up}LICENSE-CONTENT.html">CC BY-SA 4.0</a>. הקוד ברישיון <a href="{REPO}/blob/main/LICENSE">MIT</a>.</footer>
</body>
</html>
"""


def main(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, 'pages'))
    os.makedirs(os.path.join(out, 'course'))
    shutil.copytree(os.path.join(ROOT, 'course', 'img'), os.path.join(out, 'course', 'img'))
    static = os.path.join(ROOT, 'site-static')
    if os.path.isdir(static):
        for f in os.listdir(static):
            shutil.copyfile(os.path.join(static, f), os.path.join(out, f))
    urls = []
    for src, dst in sources():
        md = open(os.path.join(ROOT, src), encoding='utf-8').read()
        title, desc = title_and_description(md)
        md = fix_links(fix_math(md), src)
        url = BASE + urllib.parse.quote(dst if dst != 'index.html' else '')
        body = render(md)
        open(os.path.join(out, dst), 'w', encoding='utf-8').write(page(title, desc, body, url, dst.count('/')))
        urls.append(url)
    today = date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f'<url><loc>{html.escape(u)}</loc><lastmod>{today}</lastmod></url>' for u in urls]
    sm.append('</urlset>')
    open(os.path.join(out, 'sitemap.xml'), 'w', encoding='utf-8').write('\n'.join(sm) + '\n')
    open(os.path.join(out, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
    open(os.path.join(out, '.nojekyll'), 'w').close()
    print(f'built {len(urls)} pages into {out}')


if __name__ == '__main__':
    main(sys.argv[1])
