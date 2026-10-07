"""⚡ Super JinX auto setup: host, config name and ready subscription link."""
import json, os, sys, time, urllib.parse, urllib.request, urllib.error

API = "http://127.0.0.1:8000/api"
DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
NAME = os.environ.get("CONFIG_NAME", "Jinx | 𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫")
USER = os.environ.get("DEFAULT_USER", "superjinx")
WS = os.environ.get("WS_PATH", "/jinx")
ADDRESS = os.environ.get("CLEAN_IP") or DOMAIN


def call(method, path, data=None, token=None, form=False):
    headers = {"Accept": "application/json"}
    body = None
    if data is not None:
        if form:
            body = urllib.parse.urlencode(data).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(API + path, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read() or b"null")


def main():
    if not DOMAIN:
        print("⚠️  Bootstrap skipped: generate a Railway domain and redeploy.", flush=True)
        return
    token = None
    # Use only the public API as the compatibility boundary.
    for _ in range(90):
        try:
            token = call("POST", "/admin/token", {
                "username": os.environ["PANEL_USERNAME"],
                "password": os.environ["PANEL_PASSWORD"],
            }, form=True)["access_token"]
            break
        except urllib.error.HTTPError as exc:
            if exc.code in (400, 401, 403):
                print("❌ Bootstrap: admin authentication failed; check ADMIN_USERNAME/ADMIN_PASSWORD", flush=True)
                return
            time.sleep(2)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            time.sleep(2)
    if not token:
        print("❌ Bootstrap: Marzban API did not become ready", flush=True)
        return

    call("PUT", "/hosts", {"JINX": [{
        "remark": NAME, "address": ADDRESS, "port": 443,
        "sni": DOMAIN, "host": DOMAIN, "path": WS,
        "security": "tls", "alpn": "http/1.1", "fingerprint": "chrome",
        "allowinsecure": False, "is_disabled": False,
    }]}, token)

    try:
        user = call("GET", f"/user/{USER}", token=token)
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
        user = call("POST", "/user", {
            "username": USER, "status": "active", "expire": None, "data_limit": 0,
            "proxies": {"vless": {"flow": ""}},
            "inbounds": {"vless": ["JINX"]},
            "note": "Auto created | t.me/Super_Jinx",
        }, token)

    sub = user["subscription_url"]
    if sub.startswith("/"):
        sub = f"https://{DOMAIN}{sub}"
    print("\n" + "═" * 60)
    print("⚡ 𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫 is ready  |  t.me/Super_Jinx")
    print(f"🖥  Panel : https://{DOMAIN}/dashboard/")
    print(f"🔗 Sub   : {sub}")
    print("═" * 60 + "\n", flush=True)


try:
    main()
except Exception as exc:  # never crash the panel because of setup
    print(f"❌ Bootstrap error: {exc}", flush=True)
