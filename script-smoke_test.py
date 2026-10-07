#!/usr/bin/env python3
"""Local smoke checks for rendered config and a running deployment.
Run with BASE_URL=https://your-domain.up.railway.app for HTTP checks."""
import json, os, pathlib, sys, urllib.request

root = pathlib.Path(__file__).resolve().parents[1]
json.loads((root / 'config/xray_config.template.json').read_text())
assert (root / 'config/nginx.template.conf').read_text().count('__WS_PATH__') == 1
assert '__EXTRA_LISTEN__' in (root / 'config/nginx.template.conf').read_text()
base = os.getenv('BASE_URL')
if base:
    for path in ('/jinx-health', '/dashboard/'):
        req = urllib.request.Request(base.rstrip('/') + path, method='GET')
        with urllib.request.urlopen(req, timeout=15) as response:
            assert response.status in (200, 301, 302), (path, response.status)
print('smoke checks: ok')
