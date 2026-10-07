#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "❌ startup failed at line ${LINENO}" >&2' ERR
log(){ printf '[super-jinx] %s\n' "$*"; }

export PORT="${PORT:-8080}"
export WS_PATH="${WS_PATH:-/jinx}"
export CONFIG_NAME="${CONFIG_NAME:-Jinx | 𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫}"
# ADMIN_* is the public contract; PANEL_* remains a backwards-compatible alias.
export PANEL_USERNAME="${ADMIN_USERNAME:-${PANEL_USERNAME:-admin}}"
export PANEL_PASSWORD="${ADMIN_PASSWORD:-${PANEL_PASSWORD:-}}"
: "${PANEL_PASSWORD:?ADMIN_PASSWORD is required. Set it as a Railway secret.}"
export MARZBAN_ADMIN_PASSWORD="$PANEL_PASSWORD"

mkdir -p /var/lib/marzban /var/log/marzban
sed -e "s#__WS_PATH__#${WS_PATH}#g" /opt/jinx/config/xray_config.template.json > "${XRAY_JSON:?XRAY_JSON is unset}"
EXTRA_LISTEN=""
if [[ "${PORT}" != "8080" ]]; then EXTRA_LISTEN="listen ${PORT};"; fi
sed -e "s#__WS_PATH__#${WS_PATH}#g" -e "s#__EXTRA_LISTEN__#${EXTRA_LISTEN}#g" \
  /opt/jinx/config/nginx.template.conf > /etc/nginx/nginx.conf
nginx -t

cd /code
alembic upgrade head
# Existing admins are never overwritten, so a password changed in the panel persists.
python marzban-cli.py admin create --username "$PANEL_USERNAME" --sudo </dev/null >/dev/null 2>&1 || true

# Start Marzban first. Nginx and Railway health only become available after the API responds.
python main.py &
BACKEND_PID=$!
cleanup(){ kill "$BACKEND_PID" 2>/dev/null || true; }
trap cleanup EXIT INT TERM
ready=0
for _ in $(seq 1 90); do
  if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
    echo "❌ Marzban exited before becoming ready" >&2
    exit 1
  fi
  if python - <<'PY'
import urllib.request
try:
    with urllib.request.urlopen('http://127.0.0.1:8000/dashboard/', timeout=2) as r:
        raise SystemExit(0 if r.status < 500 else 1)
except Exception:
    raise SystemExit(1)
PY
  then ready=1; break; fi
  sleep 2
done
if [[ "$ready" != 1 ]]; then echo "❌ Marzban readiness timeout" >&2; exit 1; fi

nginx
log "Marzban ready; edge listening on ${PORT}"
python /opt/jinx/scripts/bootstrap.py &
wait "$BACKEND_PID"
