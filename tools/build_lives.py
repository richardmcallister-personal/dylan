#!/usr/bin/env python3
"""Song genealogies: tools/lives_src.py (hand-written) → site/data/lives/<slug>.json + index.json.

Fills the setlist.fm id (and the venue/city from the setlist data) for every life whose exact date has a
performance of that song on record, checks album slugs, and sorts lives by date.
Usage: python3 tools/build_lives.py
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from lives_src import SONGS

D = ROOT / "site" / "data"
albums = {a["s"] for a in json.load(open(D / "albums.json"))}
songs = {s["s"]: s for s in json.load(open(D / "songs.json"))}
ok = True
for slug, g in SONGS.items():
    if slug not in songs:
        print("not in songs.json:", slug); ok = False; continue
    perf = {p[0]: p for p in json.load(open(D / "song" / f"{slug}.json"))["p"]}
    out = {"song": songs[slug]["n"], **g, "lives": []}
    for l in g["lives"]:
        l = dict(l)
        if l.get("a") and l["a"] not in albums:
            print(slug, "unknown album", l["a"]); ok = False
        p = perf.get(l["d"]) if len(l["d"]) == 10 else None
        if p:
            l["id"] = p[1]
            l["place"] = f"{p[2]}, {p[3]}"
        elif l["kind"] == "Live" and len(l["d"]) == 10:
            print(f"  {slug}: no setlist on {l['d']} ({l['place']})")
        out["lives"].append(l)
    out["lives"].sort(key=lambda l: l["d"])
    out["others"] = sorted(g.get("others", []), key=lambda o: o.get("y", 9999))
    (D / "lives" / f"{slug}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
index = sorted({*SONGS, *json.load(open(D / "lives" / "index.json"))}, key=lambda s: songs[s]["f"][0] if s in songs else "")
(D / "lives" / "index.json").write_text(json.dumps(index))
print(len(index), "songs traced" + ("" if ok else " — FIX ERRORS ABOVE"))
