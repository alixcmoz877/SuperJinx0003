# Operations Runbook

## First deploy

1. Deploy from GitHub to Railway.
2. Set `ADMIN_PASSWORD` as a secret and `PORT=8080`.
3. Add a persistent Volume at `/var/lib/marzban`.
4. Generate the Railway domain on port `8080`.
5. Wait for `/jinx-health` to return `ok`.
6. Open `/dashboard/`, log in, then change the admin password.

## Recovery

- A failed container is restarted by Railway.
- A missing or invalid secret fails fast instead of starting insecurely.
- The database survives restarts only when the Volume is attached.
- Before upgrades, use `scripts/backup.sh` inside the container or make a Volume snapshot.

## Network diagnostics

Measure from the target carrier, not only from the server:

```bash
curl -fsS https://YOUR_DOMAIN/jinx-health
ping -c 20 YOUR_DOMAIN
curl -w '\nTTFB=%{time_starttransfer}\nTOTAL=%{time_total}\n' -o /dev/null https://YOUR_DOMAIN/dashboard/
```

A 70-80 ms target is a test objective, never a guarantee. Routing, carrier, congestion, region, and client location decide the result.

## Upgrade policy

Pin a tested Marzban image tag for production instead of blindly using `latest`. Review upstream release notes, back up the database, deploy to a staging project, then restart production.

Do not implement automatic node switching from ping alone. A safe node score needs repeated samples of latency, jitter, packet loss, and throughput from the same client network; Railway's container cannot measure the user's mobile-carrier path by itself.
