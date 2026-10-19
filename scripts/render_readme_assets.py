"""Render dependency-free SVG README assets from a real synthetic CLI run.

Run from the repository root: python3 scripts/render_readme_assets.py
"""
from html import escape
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'docs/assets'
ASSETS.mkdir(parents=True, exist_ok=True)


def text(x, y, value, size=18, color='#c7d4e2', weight='400', family='Arial, sans-serif'):
    return f'<text xml:space="preserve" x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}">{escape(value)}</text>'


def canvas(title, description, height, content):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#071220"/><stop offset="1" stop-color="#102b38"/></linearGradient><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="#7fd8d1" stroke-opacity="0.045"/></pattern></defs>
<rect width="1200" height="{height}" rx="22" fill="url(#bg)"/><rect width="1200" height="{height}" rx="22" fill="url(#grid)"/>
{content}
</svg>'''

hero = '<rect x="48" y="45" width="6" height="30" rx="3" fill="#5eead4"/>'
hero += text(70,67,'GLOBAL WEALTH  /  ENGINEERING REFERENCE',16,'#5eead4','700')
hero += text(48,146,'Every number.',64,'#f1f7fb','700')
hero += text(48,217,'A traceable story.',64,'#f1f7fb','700')
hero += text(50,267,'Deterministic calculations. Visible exceptions. Recorded decisions.',23)
hero += text(50,302,'The working data foundation for a broader AI platform.',21,'#8ba9b9')
for x, label, sub in [(50,'CALCULATE','Decimal precision'),(414,'RECONCILE','Explicit tolerance'),(778,'REVIEW','Preserved evidence')]:
    hero += f'<rect x="{x}" y="350" width="340" height="88" rx="12" fill="#0d2030" stroke="#294654"/>'
    hero += text(x+22,383,label,16,'#5eead4','700') + text(x+22,414,sub,20,'#e1edf5')
hero += text(50,480,'PYTHON  /  SQLITE  /  GITHUB ACTIONS',14,'#8ba9b9','700')
hero += text(899,480,'SYNTHETIC DATA DEMO',14,'#8ba9b9','700')
(ASSETS/'hero.svg').write_text(canvas('Global Wealth AI Platform — Every number. A traceable story.', 'A local Python reference project for deterministic calculations, reconciliation, and review using synthetic data.',515,hero))

with tempfile.TemporaryDirectory() as tmp:
    env = dict(os.environ, PYTHONPATH=str(ROOT/'src'))
    def cli(*args):
        result = subprocess.run([sys.executable,'-m','wealth_platform','--db',str(Path(tmp)/'demo.sqlite3'),*args],cwd=ROOT,env=env,capture_output=True,text=True,check=True)
        return json.loads(result.stdout)
    run = cli('run','examples/exception.json','--run-id','showcase-exception','--actor','analyst','--as-of','2026-10-19T12:00:00Z')
    reviewed = cli('review','showcase-exception','--reviewer','reviewer','--decision','rejected','--evidence','Synthetic reference differs by 100 USD; investigate source.')
    assert run['result']['delta'] == '100.00'
    assert reviewed['state'] == 'rejected'

body = '<rect x="28" y="28" width="1144" height="550" rx="16" fill="#09131f" stroke="#2b4254"/>'
for x,color in [(56,'#fb7185'),(80,'#fbbf24'),(104,'#5eead4')]:
    body += f'<circle cx="{x}" cy="55" r="6" fill="{color}"/>'
body += text(133,61,'wealth_platform   /   CLI output · selected fields',16,'#91a9bd')
body += '<path d="M28 80H1172" stroke="#2b4254"/>'
lines=[
('$ python -m wealth_platform run examples/exception.json …','#5eead4'),
('  run_id          '+run['run_id'],'#d9e5ef'),
('  actual          '+run['result']['actual']+' USD','#d9e5ef'),
('  expected        '+run['result']['expected']+' USD','#d9e5ef'),
('  delta           +'+run['result']['delta']+' USD','#fbbf24'),
('  reconciliation  '+run['result']['reconciliation'],'#fbbf24'),
('  state           '+run['state'],'#d9e5ef'),
('','#d9e5ef'),
('$ python -m wealth_platform review showcase-exception …','#5eead4'),
('  decision        '+reviewed['state'],'#fb7185'),
('  reviewer        '+reviewed['review']['reviewer'],'#d9e5ef'),
('  original delta  +'+reviewed['result']['delta']+' USD · retained','#fbbf24'),
]
for index,(line,color) in enumerate(lines):
    body += text(56,120+index*34,line,20,color,family='Menlo, Consolas, monospace')
body += text(56,554,'Real fixture results. Reformatted for readability; full commands are in the README.',16,'#91a9bd')
(ASSETS/'workflow-demo.svg').write_text(canvas('A 100 USD discrepancy, from calculation to review', 'Real synthetic CLI output: actual 1000000.00 USD, expected 999900.00 USD, discrepancy 100.00 USD; a reviewer rejects the run and the original discrepancy remains recorded.',606,body))
print('Rendered docs/assets/hero.svg and workflow-demo.svg from verified demo output.')
