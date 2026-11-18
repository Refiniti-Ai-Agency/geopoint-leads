"""Copy the live geopointleads.com site into ./dist and add Geopoint tracking.

The GitHub copy of this repo is only the Vite starter template, so the real
site is whatever is live on Firebase Hosting (last deployed Apr 8, 2026).
This script mirrors that live build, adds tracking to index.html, and leaves
it in ./dist, ready for:  npx firebase-tools deploy --only hosting --project geopoint-leads

Run from the repo root:  python3 scripts/pull_live_add_tracking.py
"""
from __future__ import annotations

import pathlib
import re
import shutil
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "dist"
BASE = "https://geopoint-leads.web.app"
TRACK = ROOT / "tracking"

ASSET_RE = re.compile(r"""[`"'(=](/[A-Za-z0-9_\-/.]+\.(?:js|css|png|jpe?g|svg|webp|gif|ico|mp4|woff2?|pdf|txt|xml|json|webmanifest))""")
OPTIONAL = ["/robots.txt", "/sitemap.xml", "/icons.svg", "/favicon.ico", "/manifest.webmanifest", "/site.webmanifest"]


def get(path: str) -> tuple[bytes, str]:
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read(), r.headers.get("Content-Type", "")


def save(path: str, data: bytes) -> None:
    dest = OUT / path.lstrip("/")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    print("saved", path, len(data))


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    index, _ = get("/index.html")
    html = index.decode("utf-8")
    if "G-ME2KNBQMQ9" in html:
        raise SystemExit("Live index.html already has tracking. Stopping so nothing gets doubled.")

    seen: set[str] = set()
    queue = [m for m in ASSET_RE.findall(html)] + OPTIONAL
    while queue:
        p = queue.pop(0)
        if p in seen or p == "/index.html":
            continue
        seen.add(p)
        try:
            data, ctype = get(p)
        except Exception as e:  # noqa: BLE001
            if p not in OPTIONAL:
                print("MISSING", p, e)
            continue
        # SPA rewrite returns index.html for unknown paths; skip those
        if "text/html" in ctype and not p.endswith(".html"):
            continue
        save(p, data)
        if p.endswith((".js", ".css")):
            queue += ASSET_RE.findall(data.decode("utf-8", "ignore"))

    head = (TRACK / "head.html").read_text(encoding="utf-8")
    html = html.replace("</head>", head + "  </head>", 1)
    save("/index.html", html.encode("utf-8"))
    shutil.copy(TRACK / "tracking.js", OUT / "tracking.js")
    print("added tracking.js")
    print("\nDone. Next:  npx firebase-tools deploy --only hosting --project geopoint-leads")


if __name__ == "__main__":
    main()
