# Changelog

## 0.3.0 - 2026-10-07

- Pinned the Marzban base image instead of floating on `latest`.
- Switched bootstrap authentication to the public API only.
- Made the readiness gate backend-backed before exposing Nginx.
- Switched SQLite backup to the SQLite online backup API.

## 0.2.0 - 2026-10-07

- Simplified the public edge to one documented VLESS + WebSocket inbound.
- Added strict startup validation, Railway health check, persistent-volume guidance, and backup script.
- Removed the fragile dashboard monkey-patch and private Marzban imports.
- Added repository security, deployment, smoke-test, and operations documentation.

## 0.1.0

- Initial Railway packaging.
