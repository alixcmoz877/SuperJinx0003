# ⚡ 𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫 · Marzban on Railway

A maintainable Railway deployment wrapper around [Marzban](https://github.com/Gozargah/Marzban), with one documented VLESS + WebSocket inbound, automatic host bootstrap, persistent storage guidance, health checks, backups, and a clean GitHub structure.

**Channel:** [@Super_Jinx](https://t.me/Super_Jinx)  ·  **Config name:** `Jinx | 𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫`

> This repository configures and packages Marzban; it does not promise a specific ping, speed, uptime, or carrier compatibility. Those depend on routing and provider conditions.

## What is included

- VLESS + WebSocket behind Railway's HTTPS edge.
- Nginx proxy with `/jinx-health`, dashboard, API, and subscription routing.
- Automatic host setup and a ready subscription user after the panel API is available.
- Strict startup validation, persistent SQLite location, restart-safe admin creation, and no password reset on restart.
- Railway health check, smoke test, backup script, security policy, changelog, issue templates, and PR template.

## Deploy

1. Create a **private** GitHub repository and upload this project.
2. Deploy that repository in Railway.
3. Add Railway Variables:
   ```env
   ADMIN_PASSWORD=use-a-long-random-password
   PORT=8080
   ```
4. Add a persistent Railway Volume mounted at `/var/lib/marzban`.
5. Generate a public Railway domain on port `8080`.
6. Redeploy and wait for the health check to pass.
7. Open `https://YOUR_DOMAIN/dashboard/`, sign in with your `ADMIN_PASSWORD`, then change it again from Marzban's native admin settings/CLI if required. Do not use a shared or default password in production.

The bootstrap process prints the subscription URL in the deployment logs. Treat that URL like a password and never commit or share it publicly.

## Configuration

| Variable | Required | Default | Purpose |
|---|---:|---|---|
| `ADMIN_PASSWORD` | yes | none | Initial admin password. Secret only. |
| `ADMIN_USERNAME` | no | `admin` | Initial sudo admin username. |
| `PORT` | no | `8080` | Railway ingress port. |
| `DEFAULT_USER` | no | `superjinx` | Bootstrap subscription user. |
| `CONFIG_NAME` | no | `Jinx | 𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫` | Host remark shown in clients. |
| `WS_PATH` | no | `/jinx` | WebSocket path. |
| `CLEAN_IP` | no | Railway domain | Optional client address override. Test before use. |

## Ports and flow

```text
Client -- HTTPS/WSS :443 --> Railway edge -- :8080 --> nginx
                                                    |-- /jinx       --> Xray :10001
                                                    |-- /dashboard  --> Marzban :8000
                                                    |-- /sub       --> Marzban :8000
```

Only Railway's public ingress is exposed. Xray and Marzban bind to loopback. There is no second public tunnel in this package because adding one without a real upstream server address, credentials, and routing test would be pretend engineering.

## Quality checklist

Before production, validate: fresh deploy, login, user creation, proxy creation, subscription retrieval, V2Box/client import, restart, volume persistence, backup/restore, health check, logs, API auth, port exposure, CPU/RAM, concurrent users, latency, packet loss, and carrier-specific behavior. See [`OPERATIONS.md`](docs/OPERATIONS.md).

## Local checks

```bash
python scripts/smoke_test.py
python -m py_compile scripts/bootstrap.py
bash -n scripts/start.sh scripts/backup.sh
python -m json.tool config/xray_config.template.json >/dev/null
python -m json.tool railway.json >/dev/null
```

The Docker image is pinned to Marzban `v0.8.4`; upgrade it only after staging validation. A real Docker/Railway/client test must be run in an environment with Docker, a Railway project, a persistent Volume, and a reachable client network. This workspace cannot honestly claim those tests were run. The release gate also refuses to label a path as best from a single ping: compare latency, jitter, loss, and throughput from the actual target carrier.

## Security

Read [`SECURITY.md`](SECURITY.md). Never commit `.env`, admin passwords, JWTs, or subscription URLs. Change the initial password immediately.

## License and upstream

This wrapper is MIT-licensed. Marzban and Xray retain their own licenses and upstream terms. See [`CHANGELOG.md`](CHANGELOG.md).
