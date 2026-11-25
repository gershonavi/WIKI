#!/usr/bin/env bash
# Register a new translated article and publish it.
# Usage: tools/add.sh "Hebrew title" "English title"   (wiki/<Hebrew title>.wiki must exist)
set -euo pipefail
cd "$(dirname "$0")/.."
he="$1"; en="$2"
[ -f "wiki/$he.wiki" ] || { echo "missing wiki/$he.wiki"; exit 1; }
grep -q "^$he	" sources.tsv || printf '%s\t%s\n' "$he" "$en" >> sources.tsv
python3 - "$en" <<'EOF'
import sys, re
en = sys.argv[1]
q = open('QUEUE.md', encoding='utf-8').read()
q = q.replace(f'- [ ] {en}\n', f'- [x] {en}\n')
open('QUEUE.md', 'w', encoding='utf-8').write(q)
EOF
python3 build.py | tail -1
git add -A
git -c user.name=gershonavi -c user.email=gershonavi@users.noreply.github.com commit -qm "Add: $he ($en)"
for i in 1 2 3; do git push -q 2>/dev/null && break; sleep 3; done; git fetch -q; [ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ] || echo "PUSH FAILED"
echo "published $he"
