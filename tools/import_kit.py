#!/usr/bin/env python3
"""Import Richard's dylan-resource-kit into the site.

Usage: python3 tools/import_kit.py <path-to-dylan-resource-kit>

Writes site/covers/<slug>.webp (max 320 px) and site/data/albums.json.
The masthead and Center feature assets are maintained separately in site/assets/.
"""
import json, subprocess, sys
from pathlib import Path

kit = Path(sys.argv[1])
root = Path(__file__).resolve().parent.parent
out_cov = root / "site" / "covers"
out_cov.mkdir(parents=True, exist_ok=True)

CAT = {"studio": "studio", "live": "live", "compilation": "comp", "bootleg": "bootleg"}

albums = []
for a in json.load(open(kit / "albums.json")):
    slug = a["slug"]
    src = kit / a["cover_file"]
    dst = out_cov / f"{slug}.webp"
    subprocess.run(["convert", str(src), "-resize", "320x320>", "-quality", "82", str(dst)], check=True)
    w, h = subprocess.run(["identify", "-format", "%w %h", str(dst)], capture_output=True, text=True).stdout.split()
    status = a.get("spotify_status", "")
    exact = bool(a.get("spotify_url")) and not status.startswith(("Different edition", "Search fallback"))
    albums.append({
        "s": slug,
        "t": a["title"],
        "y": int(a["year"]),
        "c": [CAT[c] for c in a["categories"]],
        "o": a["official_url"],
        "sp": a.get("spotify_url") or None,
        "spx": exact,                       # True = exact edition on Spotify
        "ss": a.get("spotify_search"),
        "rel": a.get("spotify_related_url") or None,
        "relt": a.get("spotify_related_title") or None,
        "w": int(w), "h": int(h),
    })

albums.sort(key=lambda x: (x["y"], x["t"]))
(root / "site" / "data" / "albums.json").write_text(json.dumps(albums, ensure_ascii=False, separators=(",", ":")))
print(len(albums), "albums")
