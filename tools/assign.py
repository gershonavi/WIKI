"""usage: assign.py UNIT title [title...] -- append articles to a syllabus unit in course/units.tsv"""
import sys
unit, titles = sys.argv[1], sys.argv[2:]
p = 'course/units.tsv'
rows = open(p, encoding='utf-8').read().rstrip('\n').split('\n')
for i, r in enumerate(rows):
    f = r.split('\t')
    if f[0] == unit:
        arts = f[3].split('|') if len(f) > 3 and f[3] else []
        for t in titles:
            if t not in arts:
                arts.append(t)
        f[3:] = ['|'.join(arts)]
        rows[i] = '\t'.join(f)
        break
else:
    sys.exit(f'no unit {unit}')
open(p, 'w', encoding='utf-8').write('\n'.join(rows) + '\n')
print('unit', unit, 'ok')
