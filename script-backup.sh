#!/usr/bin/env bash
set -Eeuo pipefail
: "${BACKUP_DIR:=/var/lib/marzban/backups}"
mkdir -p "$BACKUP_DIR"
file="$BACKUP_DIR/marzban-$(date -u +%Y%m%dT%H%M%SZ).sqlite3"
python - "$file" <<'PY'
import sqlite3, sys
source = sqlite3.connect("/var/lib/marzban/db.sqlite3", timeout=30)
target = sqlite3.connect(sys.argv[1])
with target:
    source.backup(target)
target.close(); source.close()
PY
chmod 600 "$file"
find "$BACKUP_DIR" -type f -name 'marzban-*.sqlite3' -mtime +14 -delete
printf 'backup: %s\n' "$file"
