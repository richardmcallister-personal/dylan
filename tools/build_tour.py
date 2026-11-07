#!/usr/bin/env python3
"""Upcoming dates and ticket links from the official tour page (bobdylan.com/on-tour/).

Usage: python3 tools/build_tour.py
Writes site/data/tour.json: [{d, city, venue, page, tickets, vip, presale}] in date order.
Only a plain GET with an honest user agent; if the site refuses, stop and report rather than work around it.
"""
import datetime, html, json, re, urllib.request
from pathlib import Path

URL = "https://www.bobdylan.com/on-tour/"
UA = "dylan-fansite/1.0 (+https://bobdylan.app)"
out = Path(__file__).resolve().parent.parent / "site" / "data" / "tour.json"

req = urllib.request.Request(URL, headers={"user-agent": UA})
with urllib.request.urlopen(req, timeout=60) as r:
    page = r.read().decode("utf-8", "replace")

MON = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
rows = []
for line in re.split(r'<div class="line">', page)[1:]:
    date = re.search(r'<a class="date[^"]*" href="([^"]+)">\s*([^<]+?)\s*</a>', line)
    city = re.search(r'<a class="city[^"]*"[^>]*>\s*([^<]+?)\s*</a>', line)
    venue = re.search(r'<a class="venue[^"]*"[^>]*>\s*([^<]+?)\s*</a>', line)
    if not (date and city and venue):
        continue
    try:
        dd, mon, yyyy = date.group(2).split()
        iso = f"{int(yyyy):04d}-{MON[mon[:3]]:02d}-{int(dd):02d}"
    except (ValueError, KeyError):
        continue
    btn = lambda cls: next((html.unescape(u) for c, u in re.findall(r'class="tickets (status-[a-z]+)"[^>]*data-url="([^"]+)"', line) if c == cls), None)
    presale = re.search(r'<a class="presale external"[^>]*href="([^"]+)"', line)
    rows.append({
        "d": iso,
        "city": html.unescape(city.group(1)),
        "venue": html.unescape(venue.group(1)),
        "page": date.group(1),
        "tickets": btn("status-sale"),
        "vip": btn("status-vip"),
        "presale": html.unescape(presale.group(1)) if presale else None,
    })

today = datetime.date.today().isoformat()
rows = sorted({r["page"]: r for r in rows if r["d"] >= today}.values(), key=lambda r: r["d"])
if not rows:
    raise SystemExit("No dates parsed — the page layout may have changed; tour.json left as it was.")
out.write_text(json.dumps({"built": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "source": URL, "dates": rows}, ensure_ascii=False, separators=(",", ":")))
print(len(rows), "upcoming dates,", sum(1 for r in rows if r["tickets"]), "with ticket links")
