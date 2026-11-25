#!/usr/bin/env python3
"""Copy pages/*.md into a checkout of the GitHub wiki (WIKI.wiki).

Usage: python3 sync_wiki.py PATH_TO_WIKI_CHECKOUT
Run build.py first. Links are rewritten for the wiki's flat page names.
"""
import os, re, shutil, sys, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(ROOT, 'pages')
REPO = 'https://github.com/gershonavi/WIKI'
PROOFS_PAGE = urllib.parse.quote('שיטות-הוכחה')
CATS_PAGE = urllib.parse.quote('קטגוריות')
CAT_PREFIX = 'קטגוריה '


def wiki_name(title):
    return urllib.parse.quote(title.replace(' ', '-'))


def footnotes_to_list(md):
    """GitHub wikis do not render [^n] footnotes; turn them into a numbered list."""
    defs = dict(re.findall(r'^\[\^(\w+)\]: (.*)$', md, flags=re.M))
    if not defs:
        return md
    md = re.sub(r'^\[\^(\w+)\]: .*\n?', '', md, flags=re.M)
    md = re.sub(r'\[\^(\w+)\]', lambda m: f'<sup>[[{m.group(1)}]](#user-content-fn-{m.group(1)})</sup>', md)
    notes = '\n'.join(f'<a id="fn-{k}"></a>{k}. {v}  ' for k, v in defs.items())
    marker = '\n---\n'
    i = md.find(marker)
    return (md[:i] + '\n\n' + notes + '\n' + md[i:]) if i >= 0 else md + '\n\n' + notes + '\n'


def convert(md):
    md = footnotes_to_list(md)
    md = re.sub(r'\]\((?:\.\./)?categories/([^)\s]+)\.md\)', lambda m: '](' + wiki_name(CAT_PREFIX + urllib.parse.unquote(m.group(1))) + ')', md)
    md = md.replace('](../CATEGORIES.md)', '](' + CATS_PAGE + ')').replace('](CATEGORIES.md)', '](' + CATS_PAGE + ')')
    md = md.replace('](../README.md)', '](Home)')
    md = re.sub(r'\]\((?:\.\./)?(?:pages|course)/([^)\s]+)\.md\)', lambda m: '](' + wiki_name(urllib.parse.unquote(m.group(1))) + ')', md)
    md = md.replace('](../COURSE.md)', '](%D7%A7%D7%95%D7%A8%D7%A1)').replace('](COURSE.md)', '](%D7%A7%D7%95%D7%A8%D7%A1)')
    md = md.replace('](../PROOFS.md)', '](' + PROOFS_PAGE + ')').replace('](PROOFS.md)', '](' + PROOFS_PAGE + ')')
    md = md.replace('](LICENSE-CONTENT.md)', f']({REPO}/blob/main/LICENSE-CONTENT.md)')
    md = re.sub(r'\]\(([^)/\s:]+)\.md\)', lambda m: '](' + wiki_name(urllib.parse.unquote(m.group(1))) + ')', md)
    md = md.replace('](../wiki/', f']({REPO}/blob/main/wiki/')
    md = md.replace('](LICENSE)', f']({REPO}/blob/main/LICENSE)')
    return md


def main(dest):
    page_titles = sorted(f[:-3] for f in os.listdir(PAGES) if f.endswith('.md'))
    for t in page_titles:
        md = open(os.path.join(PAGES, t + '.md'), encoding='utf-8').read()
        md = re.sub(r'^# .*\n\n', '', md, count=1)  # the wiki shows the title itself
        open(os.path.join(dest, t + '.md'), 'w', encoding='utf-8').write(convert(md))
    readme = open(os.path.join(ROOT, 'README.md'), encoding='utf-8').read()
    home = re.sub(r'\]\(pages/([^)]+)\.md\)', lambda m: '](' + wiki_name(urllib.parse.unquote(m.group(1))) + ')', readme)
    home = re.sub(r'^# .*\n', '', home, count=1)
    home = convert(home).replace('`wiki/`', f'[`wiki/`]({REPO}/tree/main/wiki)').replace('`pages/`', f'[`pages/`]({REPO}/tree/main/pages)')
    open(os.path.join(dest, 'Home.md'), 'w', encoding='utf-8').write(home)
    course_dir = os.path.join(ROOT, 'course')
    lessons = sorted(f[:-3] for f in os.listdir(course_dir) if f.endswith('.md')) if os.path.isdir(course_dir) else []
    img_src = os.path.join(course_dir, 'img')
    if os.path.isdir(img_src):  # figures of the exercises
        os.makedirs(os.path.join(dest, 'img'), exist_ok=True)
        for f in os.listdir(img_src):
            shutil.copyfile(os.path.join(img_src, f), os.path.join(dest, 'img', f))
    for l in lessons:
        md = open(os.path.join(course_dir, l + '.md'), encoding='utf-8').read()
        open(os.path.join(dest, l + '.md'), 'w', encoding='utf-8').write(convert(md))
    if os.path.exists(os.path.join(ROOT, 'COURSE.md')):
        md = open(os.path.join(ROOT, 'COURSE.md'), encoding='utf-8').read()
        md = re.sub(r'^# .*\n', '', md, count=1)
        open(os.path.join(dest, 'קורס.md'), 'w', encoding='utf-8').write(convert(md))
    if os.path.exists(os.path.join(ROOT, 'PROOFS.md')):
        md = open(os.path.join(ROOT, 'PROOFS.md'), encoding='utf-8').read()
        md = re.sub(r'^# .*\n', '', md, count=1)
        open(os.path.join(dest, 'שיטות-הוכחה.md'), 'w', encoding='utf-8').write(convert(md))
    cat_dir = os.path.join(ROOT, 'categories')
    cat_titles = sorted(f[:-3] for f in os.listdir(cat_dir) if f.endswith('.md')) if os.path.isdir(cat_dir) else []
    for f in os.listdir(dest):  # category pages that no longer exist
        if f.startswith(CAT_PREFIX) and f.endswith('.md') and f[len(CAT_PREFIX):-3] not in cat_titles:
            os.remove(os.path.join(dest, f))
    cat_size = {}
    for c in cat_titles:
        md = open(os.path.join(cat_dir, c + '.md'), encoding='utf-8').read()
        cat_size[c] = len(re.findall(r'^\* ', md, flags=re.M))
        md = re.sub(r'^# .*\n', '', md, count=1)
        open(os.path.join(dest, CAT_PREFIX + c + '.md'), 'w', encoding='utf-8').write(convert(md))
    if os.path.exists(os.path.join(ROOT, 'CATEGORIES.md')):
        md = open(os.path.join(ROOT, 'CATEGORIES.md'), encoding='utf-8').read()
        md = re.sub(r'^# .*\n', '', md, count=1)
        open(os.path.join(dest, 'קטגוריות.md'), 'w', encoding='utf-8').write(convert(md))
    side = ['**[דף הבית](Home)**', '', '**[הקורס](%D7%A7%D7%95%D7%A8%D7%A1)**', '']
    titles = {}
    up = os.path.join(course_dir, 'units.tsv')
    if os.path.exists(up):
        for row in open(up, encoding='utf-8').read().splitlines():
            parts = row.split('\t')
            if len(parts) >= 3 and not row.startswith('#'):
                titles[parts[2][:-3]] = parts[1]
    order = []
    if os.path.exists(up):
        for row in open(up, encoding='utf-8').read().splitlines():
            parts = row.split('\t')
            if len(parts) >= 3 and not row.startswith('#') and parts[2][:-3] in lessons:
                order.append((parts[0], parts[2][:-3]))
    side += [f'* {num}\\. [{titles.get(l, l)}]({wiki_name(l)})' for num, l in order]
    pp = os.path.join(course_dir, 'proofs.tsv')
    if os.path.exists(pp):
        ptitles = {}
        for row in open(pp, encoding='utf-8').read().splitlines():
            parts = row.split('\t')
            if len(parts) >= 3 and not row.startswith('#'):
                ptitles[parts[2][:-3]] = (parts[0], parts[1])
        side += ['', f'**[שיטות הוכחה]({PROOFS_PAGE})**', '']
        side += [f'* {ptitles[l][0]}\\. [{ptitles[l][1]}]({wiki_name(l)})' for l in lessons if l in ptitles]
    side += ['', f'**[ערכים לפי קטגוריה]({CATS_PAGE})** ({len(page_titles)})', '']
    main_cats = sorted((c for c in cat_titles if cat_size[c] >= 3), key=lambda c: (-cat_size[c], c))
    side += [f'* [{c}]({wiki_name(CAT_PREFIX + c)}) ({cat_size[c]})' for c in main_cats]
    side += [f'* [כל הקטגוריות והאינדקס א–ת]({CATS_PAGE})']
    side += ['', f'**[הריפו]({REPO})** · [האתר](https://gershonavi.github.io/WIKI/)']
    open(os.path.join(dest, '_Sidebar.md'), 'w', encoding='utf-8').write('\n'.join(side) + '\n')
    open(os.path.join(dest, '_Footer.md'), 'w', encoding='utf-8').write(
        f'התוכן מתורגם מוויקיפדיה האנגלית ומופץ ברישיון [CC BY-SA 4.0]({REPO}/blob/main/LICENSE-CONTENT.md). '
        f'הקוד ברישיון [MIT]({REPO}/blob/main/LICENSE).\n')
    print(f'synced {len(page_titles)} pages')


if __name__ == '__main__':
    main(sys.argv[1])
