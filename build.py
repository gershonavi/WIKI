#!/usr/bin/env python3
"""Convert Hebrew Wikipedia wikitext in wiki/*.wiki to GitHub Markdown in pages/*.md.

Hebrew templates are expanded or simplified before pandoc runs, so that
footnotes, math and links render on GitHub. Run: python3 build.py
"""
import os, re, subprocess, urllib.parse, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(ROOT, 'wiki'), os.path.join(ROOT, 'pages')


def split_template(s, i):
    """s[i:] starts with '{{'; return (end_index, inner) with balanced braces."""
    depth, j = 0, i
    while j < len(s):
        if s.startswith('{{', j):
            depth += 1; j += 2; continue
        if s.startswith('}}', j):
            depth -= 1; j += 2
            if depth == 0:
                return j, s[i + 2:j - 2]
            continue
        j += 1
    return len(s), s[i + 2:]


def split_params(inner):
    parts, depth, cur, k = [], 0, '', 0
    while k < len(inner):
        two = inner[k:k + 2]
        if two in ('{{', '[['):
            depth += 1; cur += two; k += 2; continue
        if two in ('}}', ']]'):
            depth -= 1; cur += two; k += 2; continue
        c = inner[k]
        if c == '|' and depth == 0:
            parts.append(cur); cur = ''
        else:
            cur += c
        k += 1
    parts.append(cur)
    name = parts[0].strip()
    pos, named = [], {}
    for p in parts[1:]:
        m = re.match(r'\s*([^=\[\]{}<>]+?)\s*=(.*)$', p, re.S)
        if m:
            named[m.group(1).strip()] = m.group(2)
        else:
            pos.append(p)
    return name, pos, named


def render_template(name, pos, named):
    get = lambda k, d='': named.get(k, pos[int(k) - 1] if k.isdigit() and len(pos) >= int(k) else d)
    if name == 'הערה':
        text = expand(get('1'))
        ref = named.get('שם')
        if text.strip():
            return f'<ref name="{ref}">{text}</ref>' if ref else f'<ref>{text}</ref>'
        return f'<ref name="{ref}"/>' if ref else ''
    if name in ('הערות שוליים', 'reflist', 'Reflist'):
        return '<references/>'
    if name == 'DOI':
        d = get('1').strip()
        return f'[https://doi.org/{d} doi:{d}]'
    if name.lower() == 'arxiv':
        a = get('1').strip()
        return f'[https://arxiv.org/abs/{a} arXiv:{a}]'
    if name == 'ערך מורחב':
        links = ', '.join(f'[[{p.strip()}]]' for p in pos if p.strip())
        return f"''ערך מורחב: {links}''"
    if name == 'אנגלית':
        return '(באנגלית)'
    if name == 'משוואה':
        return expand(get('1'))
    if name in ('ltr', 'שמאל'):
        return expand(get('1'))
    if name == 'MathWorld':
        return '[https://mathworld.wolfram.com MathWorld]'
    if name == 'פירוש נוסף':
        return ''
    if name == 'מדען':
        return ''
    if name == 'דרוש מקור':
        return ''
    return ''  # unknown templates are dropped


def expand(s):
    out, i = [], 0
    while True:
        j = s.find('{{', i)
        if j < 0:
            out.append(s[i:]); break
        out.append(s[i:j])
        end, inner = split_template(s, j)
        name, pos, named = split_params(inner)
        out.append(render_template(name, pos, named))
        i = end
    return ''.join(out)


def strip_file_links(s):
    """Replace [[קובץ:...]] with an image from Wikimedia Commons."""
    out, i = [], 0
    while True:
        m = re.search(r'\[\[(?:קובץ|File|Image|תמונה):', s[i:])
        if not m:
            out.append(s[i:]); break
        j = i + m.start(); out.append(s[i:j])
        depth, k = 0, j
        while k < len(s):
            if s.startswith('[[', k): depth += 1; k += 2; continue
            if s.startswith(']]', k):
                depth -= 1; k += 2
                if depth == 0: break
                continue
            k += 1
        inner = s[j + 2:k - 2]
        parts = inner.split('|')
        fname = parts[0].split(':', 1)[1].strip()
        caption = parts[-1] if len(parts) > 1 else ''
        caption = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', caption)
        url = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(fname.replace(' ', '_'))
        cap = caption.replace('"', "'")
        out.append(f'<img src="{url}" alt="{cap}" width="320">\n\n')
        i = k
    return ''.join(out)


def preprocess(text):
    cats = re.findall(r'\[\[קטגוריה:([^\]|]+)(?:\|[^\]]*)?\]\]', text)
    text = re.sub(r'\[\[קטגוריה:[^\]]*\]\]\n?', '', text)
    text = re.sub(r'__[A-Z]+__', '', text)
    text = strip_file_links(text)
    text = expand(text)
    text = text.replace('<div dir="ltr">', '').replace('</div>', '')
    return text, cats


def fix_math(md):
    """Use GitHub's robust math syntax: ```math blocks and $`...`$ inline."""
    md = re.sub(r'\$\$(.+?)\$\$', lambda m: '\n\n```math\n' + m.group(1).strip() + '\n```\n\n', md, flags=re.S)
    parts = re.split(r'(```math\n.*?\n```)', md, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<![\\$])\$(?!\$)([^$\n]+?)(?<!\\)\$', lambda m: '$`' + m.group(1) + '`$', parts[i])
    return ''.join(parts)


def fix_links(md, local):
    def repl(m):
        label, target = m.group(1), m.group(2)
        if re.match(r'https?://', target):
            return m.group(0)
        t = urllib.parse.unquote(target).replace('_', ' ').split('#')[0].strip()
        if t in local:
            return f'[{label}]({urllib.parse.quote(t)}.md)'
        return f'[{label}](https://he.wikipedia.org/wiki/{urllib.parse.quote(t.replace(" ", "_"))})'
    md = re.sub(r'\[([^\]]*)\]\((\S+?) "wikilink"\)', repl, md)
    return re.sub(r'\[([^\]]*)\]\(([^)\s]+)\)', repl, md)


def write_index(files, sources):
    bycat = {}
    for f in files:
        title = f[:-5]
        text = open(os.path.join(SRC, f), encoding='utf-8').read()
        cats = re.findall(r'\[\[קטגוריה:([^\]|]+)', text) or ['שונות']
        bycat.setdefault(cats[0].strip(), []).append(title)
    lines = ['# ויקי תורת המספרים בעברית', '',
             'אוסף ערכים בתורת המספרים, מתורגמים לעברית מוויקיפדיה האנגלית, וקורס מסודר המבוסס עליהם.', '',
             '**[לקורס: תורת המספרים בעברית, לפי סדר הלימוד](COURSE.md)**', '',
             'כל ערך מופיע פעמיים: כדף לקריאה בתיקייה `pages/`, וכקוד ויקי בתיקייה `wiki/` שאפשר להעתיק ישירות לוויקיפדיה.', '',
             '**רישיון:** התוכן ברישיון [CC BY-SA 4.0](LICENSE-CONTENT.md), כמו ויקיפדיה, כך שכל אחד רשאי להעתיק אותו בחזרה לוויקיפדיה עם ציון המקור. '
             'הקוד (סקריפט ההמרה) ברישיון [MIT](LICENSE).', '',
             '**הערה:** לפני העתקת ערך לוויקיפדיה, כדאי לעבור עליו ולוודא שהניסוח והעובדות תואמים את מקורותיו.', '',
             f'## ערכים ({len(files)})', '']
    for cat in sorted(bycat):
        lines += [f'### {cat}', '']
        for t in sorted(bycat[cat]):
            en = sources.get(t)
            lines.append(f'* [{t}](pages/{urllib.parse.quote(t)}.md)' + (f' – {en}' if en else ''))
        lines.append('')
    lines += ['## בנייה מחדש', '', '```', 'python3 build.py', '```', '',
              'הסקריפט ממיר כל קובץ `wiki/*.wiki` לדף Markdown ב-`pages/` (דורש pandoc).', '']
    open(os.path.join(ROOT, 'README.md'), 'w', encoding='utf-8').write('\n'.join(lines))


def write_course(local):
    path = os.path.join(ROOT, 'course', 'units.tsv')
    if not os.path.exists(path):
        return
    lines = ['# קורס: תורת המספרים בעברית', '',
             'הקורס בנוי לפי הסדר שבו הידע נבנה: כל יחידה נשענת על היחידות שלפניה.',
             'בכל יחידה יש שיעור עם הסבר, דוגמאות פתורות שלב אחר שלב ותרגילים עם פתרונות, ואחריו רשימת ערכים להעמקה.', '',
             'מקרא: ערכים בלי סימון נמצאים בוויקי הזה; ↗ – ערך קיים בוויקיפדיה העברית; ⏳ – ערך שעדיין בתור התרגום.', '']
    assigned = set()
    for row in open(path, encoding='utf-8').read().splitlines():
        if not row.strip() or row.startswith('#'):
            continue
        num, title, lesson, arts = row.split('\t')
        lp = os.path.join(ROOT, 'course', lesson)
        head = f'## יחידה {num}: {title}'
        lines.append(head)
        lines.append('')
        if os.path.exists(lp):
            lines.append(f'**[שיעור {num}: {title}](course/{urllib.parse.quote(lesson)})**')
        else:
            lines.append(f'שיעור {num}: {title} (בכתיבה)')
        lines.append('')
        items = []
        for a in arts.split('|'):
            a = a.strip()
            if not a:
                continue
            if a.startswith('he:'):
                t = a[3:]
                items.append(f'[{t}](https://he.wikipedia.org/wiki/{urllib.parse.quote(t.replace(" ", "_"))}) ↗')
            elif a.startswith('en:'):
                t = a[3:]
                items.append(f'{t} ⏳')
            else:
                assigned.add(a)
                if a in local:
                    items.append(f'[{a}](pages/{urllib.parse.quote(a)}.md)')
                else:
                    items.append(f'{a} ⏳')
        lines.append('ערכים: ' + ' · '.join(items))
        lines.append('')
    missing = sorted(local - assigned)
    if missing:
        lines += ['## ערכים נוספים', '', 'ערכים בוויקי שעוד לא שובצו ביחידה:', ''] + [f'* [{t}](pages/{urllib.parse.quote(t)}.md)' for t in missing] + ['']
        print('unassigned:', ', '.join(missing))
    open(os.path.join(ROOT, 'COURSE.md'), 'w', encoding='utf-8').write('\n'.join(lines))


def main():
    os.makedirs(OUT, exist_ok=True)
    files = sorted(f for f in os.listdir(SRC) if f.endswith('.wiki'))
    sources = {}
    sp = os.path.join(ROOT, 'sources.tsv')
    if os.path.exists(sp):
        for line in open(sp, encoding='utf-8').read().splitlines()[1:]:
            he, en = (line.split('\t') + [''])[:2]
            sources[he] = en.strip()
    local = {f[:-5] for f in files}
    failed = []
    for f in files:
        title = f[:-5]
        text = open(os.path.join(SRC, f), encoding='utf-8').read()
        pre, cats = preprocess(text)
        r = subprocess.run(['pandoc', '-f', 'mediawiki', '-t', 'gfm', '--wrap=none'],
                           input=pre, capture_output=True, text=True)
        if r.returncode != 0:
            failed.append((title, r.stderr[:200])); continue
        md = fix_math(fix_links(r.stdout.replace('<references/>', ''), local))
        head = f'# {title}\n\n'
        foot = ''
        if cats:
            foot += '\n\n---\nקטגוריות: ' + ' · '.join(cats) + '\n'
        en = sources.get(title)
        src = (f'מבוסס על הערך [{en}](https://en.wikipedia.org/wiki/{urllib.parse.quote(en.replace(" ", "_"))}) '
               f'בוויקיפדיה האנגלית ([היסטוריית העריכות ומחברים](https://en.wikipedia.org/w/index.php?title={urllib.parse.quote(en.replace(" ", "_"))}&action=history)). ') if en else ''
        foot += ('\n\n---\n<sub>' + src + 'התוכן מופץ ברישיון [CC BY-SA 4.0]'
                 '(https://creativecommons.org/licenses/by-sa/4.0/), ואפשר להעתיק אותו בחזרה לוויקיפדיה. '
                 f'[קוד הוויקי של הדף](../wiki/{urllib.parse.quote(f)})</sub>\n')
        open(os.path.join(OUT, title + '.md'), 'w', encoding='utf-8').write(head + md + foot)
    write_index(files, sources)
    write_course(local)
    print(f'built {len(files) - len(failed)} / {len(files)}')
    for t, e in failed:
        print('FAILED', t, e)


if __name__ == '__main__':
    main()
