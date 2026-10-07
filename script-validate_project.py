#!/usr/bin/env python3
"""Static release gate. It does not fake latency or claim a live Railway test."""
from pathlib import Path
import json, re, sys
ROOT = Path(__file__).resolve().parents[1]
errors=[]; warnings=[]
def read(path, needle=None):
 p=ROOT/path
 if not p.exists(): errors.append(f'missing: {path}'); return ''
 s=p.read_text()
 if needle and needle not in s: errors.append(f'{path}: missing {needle}')
 return s

docker=read(Path('Dockerfile'),'COPY scripts/')
start=read(Path('scripts/start.sh'),'nginx -t')
nginx=read(Path('config/nginx.template.conf'),'__WS_PATH__')
readme=read(Path('README.md'),'ADMIN_PASSWORD')
read(Path('docs/OPERATIONS.md'),'70-80 ms')
read(Path('SECURITY.md'),'Never commit')
for name in ('railway.json','config/xray_config.template.json'):
 try: json.loads(read(Path(name)))
 except json.JSONDecodeError as e: errors.append(f'{name}: invalid JSON: {e}')
if 'latest' in docker: errors.append('Docker image uses latest; pin a tested Marzban tag before release.')
if re.search(r'PANEL_PASSWORD\s*=\s*admin', read(Path('.env.example'))): errors.append('.env.example contains insecure admin password')
if 'admin/admin' in readme: errors.append('README advertises admin/admin')
if '__EXTRA_LISTEN__' not in nginx: errors.append('nginx template has no Railway PORT placeholder')
if 'sub_filter' in nginx or 'jinx-ui' in docker: errors.append('dashboard monkey-patching is present')
if 'create_admin_token' in read(Path('scripts/bootstrap.py')): errors.append('bootstrap imports private Marzban internals')
if '--password' in start and 'marzban-cli.py admin create' in start: errors.append('CLI password passed as an unsupported flag')
if 'sqlite3.connect' not in read(Path('scripts/backup.sh')): errors.append('backup does not use SQLite backup API')
if 'proxy_pass http://127.0.0.1:8000/dashboard/' not in nginx: errors.append('health check is not backend-backed')
if errors:
 print('RELEASE GATE: FAIL'); print('\n'.join('- '+x for x in errors)); sys.exit(1)
print('RELEASE GATE: PASS')
for w in warnings: print('WARNING: '+w)
