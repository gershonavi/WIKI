"""Print the JS snippet that checks a wiki file's links on he.wikipedia (run it in a he.wikipedia tab)."""
import re, sys, json
s = open(sys.argv[1], encoding='utf-8').read()
ts = sorted({t.strip() for t in re.findall(r'\[\[([^\]|#]+)', s) if not re.match(r'(קובץ|קטגוריה|File|Category):', t)})
print("const ts=" + json.dumps(ts, ensure_ascii=False) + ";const out=[];for(let i=0;i<ts.length;i+=40){const r=await fetch('/w/api.php?action=query&format=json&redirects=1&titles='+encodeURIComponent(ts.slice(i,i+40).join('|'))).then(r=>r.json());for(const p of Object.values(r.query.pages)) if(p.missing!==undefined) out.push('MISSING '+p.title);}out.join(' ;; ')||'all ok'")
