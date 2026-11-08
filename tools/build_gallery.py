#!/usr/bin/env python3
"""Gallery data and thumbnails from Richard's photos in site/assets/dylan-concert-photos/.

Usage: python3 tools/build_gallery.py
File names are NNN-YYYY-place-slug.jpg (photos/ = full frame, square-photos/ = square crops).
Writes thumbs/NNN.webp (360 px square, centre crop of the full frame) and site/data/gallery.json:
  [{n, y, f, sq, th, place, venue, city, country, show?, shows?}]  in chronological order.
Shows are matched to setlist.fm data by year + city: one match → show id, several → count (link to that year).
"""
import json, re, subprocess, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "site" / "assets" / "dylan-concert-photos"
THUMBS = BASE / "thumbs"
THUMBS.mkdir(exist_ok=True)

COUNTRIES = [
    ("northern-ireland", "Northern Ireland"), ("western-australia", "Australia"), ("usa", "USA"), ("england", "England"),
    ("wales", "Wales"), ("scotland", "Scotland"), ("ireland", "Ireland"), ("france", "France"), ("spain", "Spain"),
    ("italy", "Italy"), ("greece", "Greece"), ("slovakia", "Slovakia"), ("portugal", "Portugal"), ("australia", "Australia"),
    ("denmark", "Denmark"), ("norway", "Norway"), ("taiwan", "Taiwan"), ("germany", "Germany"), ("sweden", "Sweden"),
    ("singapore", "Singapore"), ("israel", "Israel"), ("canada", "Canada"), ("austria", "Austria"),
    ("netherlands", "Netherlands"), ("belgium", "Belgium"),
]
US_STATES = ["new-york", "michigan", "washington", "oregon", "south-dakota", "rhode-island", "tennessee", "california",
             "wisconsin", "iowa", "missouri", "illinois", "maryland", "pennsylvania", "louisiana", "new-jersey",
             "massachusetts", "ontario"]
FIX = {"alg-s": "algés", "f-rth": "fürth", "le-d-me": "le-dôme", "benic-ssim": "benicàssim", "woodstock-94": "woodstock-'94",
       "o2": "o2", "jfk": "jfk", "bbc": "bbc", "salzburgarena": "salzburgarena"}
SMALL = {"of", "de", "at", "di", "the", "near", "upon", "le", "on", "and"}
UPPER = {"bbc", "jfk", "o2", "usa"}

# Places where the slug alone can't say which words are the venue and which the city.
SPLIT = {
    "forest-hills-tennis-stadium-queens-new-york-city": ("Forest Hills Tennis Stadium", "Queens, New York City"),
    "beacon-theatre-new-york-city": ("Beacon Theatre", "New York City"),
    "carnegie-hall-new-york-city": ("Carnegie Hall", "New York City"),
    "slane-castle-county-meath": ("Slane Castle", "County Meath"),
    "dundonald-ice-bowl-near-belfast": ("Dundonald Ice Bowl", "near Belfast"),
    "hop-farm-paddock-wood": ("Hop Farm", "Paddock Wood"),
    "glastonbury-festival-pilton": ("Glastonbury Festival", "Pilton"),
    "nowlan-park-kilkenny": ("Nowlan Park", "Kilkenny"),
    "arena-di-verona-verona": ("Arena di Verona", "Verona"),
    "terme-di-caracalla-rome": ("Terme di Caracalla", "Rome"),
    "castello-scaligero-verona-province": ("Castello Scaligero", "Verona province"),
    "piazza-grande-modena": ("Piazza Grande", "Modena"),
    "le-bourget-airport-near-paris": ("Le Bourget Airport", "near Paris"),
    "pavillon-de-paris-paris": ("Pavillon de Paris", "Paris"),
    "poble-espanyol-barcelona": ("Poble Espanyol", "Barcelona"),
    "festival-internacional-de-benicàssim-benicàssim": ("Festival Internacional de Benicàssim", "Benicàssim"),
    "sofiero-castle-helsingborg": ("Sofiero Castle", "Helsingborg"),
    "ramat-gan-stadium-ramat-gan": ("Ramat Gan Stadium", "Ramat Gan"),
    "entertainment-centre-wollongong": ("Entertainment Centre", "Wollongong"),
    "braehead-arena-glasgow-area": ("Braehead Arena", "Glasgow area"),
    "arvest-bank-theatre-at-the-midland-kansas-city": ("Arvest Bank Theatre at the Midland", "Kansas City"),
    "eastern-michigan-university-ypsilanti": ("Eastern Michigan University", "Ypsilanti"),
    "jazz-fest-new-orleans": ("Jazz Fest", "New Orleans"),
    "woodstock-'94-saugerties": ("Woodstock '94", "Saugerties"),
    "melbourne-airport": ("Melbourne Airport", ""),
    "brisbane-airport": ("Brisbane Airport", ""),
    "roxy-hearts-diner-portland": ("Roxy Hearts Diner", "Portland"),
    "bbc-studios-london": ("BBC Studios", "London"),
    "bluesfest-byron-bay": ("Bluesfest", "Byron Bay"),
    "fremantle-western-australia": ("", "Fremantle, Western Australia"),
    "convention-hall-asbury-park": ("Convention Hall", "Asbury Park"),
    "pause-guitare-albi": ("Pause Guitare", "Albi"),
}
VENUE_WORDS = r"(festival|stadium|arena|park|centre|center|hall|theatre|theater|academy|club|castle|bowl|forum|apollo|spektrum|palladium|pavilion|kohl|bumbershoot|bonnaroo|edgefield|stadthalle|palatrussardi|salzburgarena|ahoy|dôme|o2|summer|rock|blues|pause-guitare)"


def title(slug):
    words = slug.split("-")
    out = []
    for i, w in enumerate(words):
        if w in UPPER:
            out.append(w.upper())
        elif i and w in SMALL:
            out.append(w)
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out).replace("Woodstock '94", "Woodstock '94")


def parse(rest):
    s = rest
    for k, v in FIX.items():
        s = re.sub(rf"(?<![^-]){re.escape(k)}(?![^-])", v, s)
    country = ""
    for suf, name in COUNTRIES:
        if s == suf or s.endswith("-" + suf):
            country, s = name, s[: -len(suf)].rstrip("-")
            if suf == "western-australia":
                s = (s + "-western-australia").strip("-")
            break
    if not country and s == "singapore":
        country, s = "Singapore", ""
    state = ""
    if country in ("USA", "Canada"):
        for st in US_STATES:
            if s.endswith("-" + st) and not s.endswith("new-york-city"):
                state, s = title(st), s[: -len(st) - 1]
                break
    if s in SPLIT:
        venue, city = SPLIT[s]
    else:
        parts = s.split("-") if s else []
        # venue = words up to the last venue-ish word; the rest is the city
        cut = 0
        for i, w in enumerate(parts):
            if re.fullmatch(VENUE_WORDS, w):
                cut = i + 1
        if cut and cut < len(parts):
            venue, city = title("-".join(parts[:cut])), title("-".join(parts[cut:]))
        else:
            venue, city = "", title(s)
    if not city and country == "Singapore":
        city = "Singapore"
    if state:
        city = f"{city}, {state}" if city else state
    place = ", ".join(x for x in [venue, city, country if country != city else ""] if x)
    return venue, city, country, place


def norm(x):
    x = unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]+", " ", x).strip()


years_cache = {}


def shows_for(y, city, venue):
    if y not in years_cache:
        f = ROOT / "site" / "data" / "years" / f"{y}.json"
        years_cache[y] = json.load(open(f)) if f.exists() else []
    c = norm(city.split(",")[0].replace("near ", "").replace(" area", "")) if city else ""
    v = norm(venue)
    hits = []
    for s in years_cache[y]:
        sc, sv = norm(s.get("c", "")), norm(s.get("v", ""))
        if (c and (c in sc or sc in c) and len(sc) > 2) or (v and len(v) > 5 and (v in sv or sv in v)):
            hits.append(s)
    if v and len(hits) > 1:  # prefer venue matches when there are several shows in the city
        vh = [s for s in hits if v in norm(s.get("v", "")) or norm(s.get("v", "")) in v]
        hits = vh or hits
    return hits


out = []
for f in sorted((BASE / "photos").glob("*.jpg")):
    m = re.match(r"^(\d+)-(\d{4})-(.+)\.jpg$", f.name)
    if not m:
        continue
    n, y, rest = int(m.group(1)), int(m.group(2)), m.group(3)
    venue, city, country, place = parse(rest)
    sq = BASE / "square-photos" / f.name
    th = THUMBS / f"{m.group(1)}.webp"
    if not th.exists():
        subprocess.run(["convert", str(f), "-resize", "360x360^", "-gravity", "center", "-extent", "360x360", "-quality", "78", str(th)], check=True)
    w, h = subprocess.run(["identify", "-format", "%w %h", str(f)], capture_output=True, text=True).stdout.split()
    rec = {"n": n, "y": y, "f": f.name, "w": int(w), "h": int(h), "place": place, "venue": venue, "city": city, "country": country}
    hits = shows_for(y, city, venue)
    if len(hits) == 1:
        rec["show"] = {"id": hits[0]["id"], "d": hits[0]["d"], "v": hits[0]["v"]}
    elif hits:
        rec["shows"] = len(hits)
    out.append(rec)

out.sort(key=lambda r: (r["y"], r.get("show", {}).get("d", ""), r["n"]))
(ROOT / "site" / "data" / "gallery.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print(len(out), "photos;", sum(1 for r in out if "show" in r), "matched to one show;", sum(1 for r in out if "shows" in r), "to several")
