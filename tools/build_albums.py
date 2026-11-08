#!/usr/bin/env python3
"""Album facts for /album/ pages, from Wikipedia (via the site's Worker) with MusicBrainz as fallback.

Usage: python3 tools/build_albums.py [--base https://bobdylan.app]

Reads tools/wiki_titles.json (slug -> English Wikipedia title, or null when there is no article) and
site/data/albums.json. Writes site/data/album/<slug>.json with:
  released, recorded, studios, venues, producers, label, length, genres   (infobox)
  personnel: [{group, name, role}]                                          (Personnel section)
  tracks:    [{side, n, title, writer, length, note}]                       (track listing templates)
  charts:    [{chart, peak, year}]                                          (Charts section)
  certs:     [{region, award}]                                              (Certifications)
  wiki: {title, url, revid}                                                 (source, CC BY-SA)
Only facts and titles are taken — never lyrics or article prose. Editorial text lives in data/album_notes.json.
"""
import argparse, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
import mwparserfromhell as mw

ap = argparse.ArgumentParser()
ap.add_argument("--base", default="https://bobdylan.app")
ap.add_argument("--cache", default="/tmp/wiki")
args = ap.parse_args()

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "data" / "album"
OUT.mkdir(parents=True, exist_ok=True)
TITLES = json.load(open(ROOT / "tools" / "wiki_titles.json"))
ALBUMS = json.load(open(ROOT / "site" / "data" / "albums.json"))
UA = "bobdylan.app-builder/1.0 (+https://bobdylan.app)"
cache = Path(args.cache)
cache.mkdir(exist_ok=True)


def wiki(title):
    f = cache / (urllib.parse.quote(title, safe="") + ".json")
    if f.exists():
        return json.load(open(f))
    u = f"{args.base}/api/wiki?t={urllib.parse.quote(title)}"
    with urllib.request.urlopen(urllib.request.Request(u, headers={"user-agent": UA}), timeout=60) as r:
        d = json.load(r)
    f.write_text(json.dumps(d))
    time.sleep(0.4)
    return d


def plain(x):
    """Wikitext fragment -> plain text."""
    if x is None:
        return ""
    s = str(x)
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    code = mw.parse(s)
    for t in code.filter_templates(recursive=False):
        n = str(t.name).strip().lower()
        try:
            if n in ("hlist", "flatlist", "plainlist", "ubl", "unbulleted list", "flat list"):
                items = [plain(p.value) for p in t.params if not p.showkey]
                code.replace(t, "; ".join(i for i in items if i))
            elif n in ("start date", "start-date", "release date", "start date and age", "end date"):
                v = [str(p.value).strip() for p in t.params if not p.showkey]
                MON = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                if len(v) >= 3 and v[1].isdigit() and v[2].isdigit():
                    code.replace(t, f"{MON[int(v[1])]} {int(v[2])}, {v[0]}")
                elif len(v) >= 2 and v[1].isdigit():
                    code.replace(t, f"{MON[int(v[1])]} {v[0]}")
                else:
                    code.replace(t, v[0] if v else "")
            elif n == "duration":
                h = t.get("h").value.strip() if t.has("h") else ""
                m = t.get("m").value.strip() if t.has("m") else "0"
                sec = t.get("s").value.strip() if t.has("s") else "0"
                code.replace(t, (f"{h}:" if h else "") + f"{int(m or 0)}:{int(sec or 0):02d}")
            elif n in ("nowrap", "nobr", "small", "lang", "noitalic", "not a typo"):
                v = [p.value for p in t.params if not p.showkey]
                code.replace(t, plain(v[-1]) if v else "")
            elif n in ("'", "'s"):
                code.replace(t, "'")
            elif n in ("ndash", "snd", "spaced ndash"):
                code.replace(t, " – ")
            else:
                code.remove(t)
        except ValueError:
            pass
    s = code.strip_code(normalize=True, collapse=True)
    s = s.replace("&nbsp;", " ").replace(" ", " ")
    s = re.sub(r"'{2,}", "", s)
    s = re.sub(r"\s+", " ", s).strip(" ,;")
    return s


def section(code, name_re):
    for sec in code.get_sections(levels=[2, 3], include_lead=False):
        head = sec.filter_headings()[0]
        if re.search(name_re, str(head.title).strip(), re.I):
            return sec
    return None


def infobox(code):
    for t in code.filter_templates():
        if str(t.name).strip().lower().startswith("infobox album"):
            return t
    return None


def ib(t, *names):
    for n in names:
        if t is not None and t.has(n):
            v = plain(t.get(n).value)
            if v:
                return v
    return ""


def split_list(s):
    return [x.strip() for x in re.split(r";|\s*,\s*(?=[A-Z])|\s+and\s+(?=[A-Z])", s) if x.strip()]


def personnel(code):
    sec = section(code, r"^personnel|^credits")
    if not sec:
        return []
    out, group = [], ""
    body = str(sec).split("\n", 1)[1] if "\n" in str(sec) else ""
    for line in body.split("\n"):
        L = line.strip()
        if not L:
            continue
        m = re.match(r"^=+\s*(.+?)\s*=+$", L) or re.match(r"^'''(.+?)'''\s*:?$", L) or re.match(r"^;\s*(.+)$", L)
        if m:
            group = plain(m.group(1)).rstrip(":")
            continue
        if L.startswith("*"):
            t = plain(L.lstrip("*").strip())
            if not t:
                continue
            parts = re.split(r"\s+[–—-]\s+|\s*:\s+", t, maxsplit=1)
            name, role = (parts[0], parts[1]) if len(parts) == 2 else (t, "")
            if len(name) > 80:
                continue
            out.append({"group": group, "name": name.strip(), "role": role.strip()})
    return out[:120]


def tracks(code):
    out = []
    for t in code.filter_templates():
        if str(t.name).strip().lower().replace("_", " ") not in ("track listing", "tracklist", "track list"):
            continue
        side = plain(t.get("headline").value) if t.has("headline") else ""
        allw = plain(t.get("all_writing").value) if t.has("all_writing") else ""
        allw = re.sub(r",?\s*except where noted\.?", "", allw, flags=re.I)
        extra_col = plain(t.get("extra_column").value) if t.has("extra_column") else ""
        i = 1
        while t.has(f"title{i}"):
            title = plain(t.get(f"title{i}").value)
            w = plain(t.get(f"writer{i}").value) if t.has(f"writer{i}") else ""
            note = plain(t.get(f"note{i}").value) if t.has(f"note{i}") else ""
            ln = plain(t.get(f"length{i}").value) if t.has(f"length{i}") else ""
            extra = plain(t.get(f"extra{i}").value) if t.has(f"extra{i}") else ""
            row = {"side": side, "n": i, "title": title.strip('"'), "writer": w or allw, "length": ln}
            if note:
                row["note"] = note
            if extra and re.search(r"record", extra_col, re.I):
                row["rec"] = extra
            out.append(row)
            i += 1
    return out[:400]


CHART_NAMES = {
    "billboard200": "US Billboard 200", "uk2": "UK Albums Chart", "ukalbum": "UK Albums Chart", "australia": "Australia",
    "austria": "Austria", "flanders": "Belgium (Flanders)", "wallonia": "Belgium (Wallonia)", "canada": "Canada",
    "denmark": "Denmark", "netherlands": "Netherlands", "finland": "Finland", "france": "France", "germany4": "Germany",
    "germany": "Germany", "hungary": "Hungary", "ireland": "Ireland", "italy": "Italy", "japan": "Japan (Oricon)",
    "oricon": "Japan (Oricon)", "newzealand": "New Zealand", "norway": "Norway", "portugal": "Portugal", "spain": "Spain",
    "sweden": "Sweden", "switzerland": "Switzerland", "scotland": "Scotland", "czech": "Czech Republic", "greece": "Greece",
    "poland": "Poland", "croatia": "Croatia", "lithuania": "Lithuania", "billboardcanada": "Canada", "rpm": "Canada (RPM)",
    "billboardtopcatalog": "US Top Catalog Albums", "billboardrockalbums": "US Top Rock Albums",
    "billboardfolkalbums": "US Americana/Folk Albums", "billboardvinylalbums": "US Vinyl Albums",
    "billboardtopalbumsales": "US Top Album Sales", "ukrock": "UK Rock & Metal Albums", "ukindependent": "UK Independent Albums",
    "irishindependent": "Irish Independent Albums", "billboardindependent": "US Independent Albums",
    "billboardtastemaker": "US Tastemaker Albums", "billboardchristmas": "US Holiday Albums",
}


def charts(code):
    sec = section(code, r"^charts?$|chart positions|^weekly charts|^chart performance")
    if not sec:
        return []
    out, year = [], ""
    s = str(sec)
    # walk lines of wikitables; album chart templates first
    for t in sec.filter_templates():
        n = str(t.name).strip().lower()
        if n == "album chart":
            ps = [str(p.value).strip() for p in t.params if not p.showkey]
            if len(ps) >= 2:
                key = ps[0].lower()
                out.append({"chart": CHART_NAMES.get(key, ps[0]), "peak": re.sub(r"[^0-9]", "", ps[1]) or ps[1], "year": ""})
    rows = re.split(r"\n\|-", s)
    for r in rows:
        y = re.search(r"Chart \((\d{4}(?:[–-]\d{2,4})?)\)", r)
        if y:
            year = y.group(1)
        m = re.search(r"!\s*(?:scope=\"?row\"?\s*\|)?\s*(.+?)\n\|\s*(?:style=[^|]*\|)?\s*([0-9]{1,3})\s*(?:\n|$)", r, re.S)
        if m and "album chart" not in r.lower():
            name = plain(m.group(1))
            if name and not name.lower().startswith("chart"):
                out.append({"chart": name, "peak": m.group(2), "year": year})
    # attach years to template rows by order of appearance where possible
    seen, res = set(), []
    for c in out:
        k = (c["chart"], c["peak"])
        if k in seen:
            continue
        seen.add(k)
        res.append(c)
    return res[:60]


def certs(code):
    out = []
    for t in code.filter_templates():
        if str(t.name).strip().lower() == "certification table entry":
            region = plain(t.get("region").value) if t.has("region") else ""
            award = plain(t.get("award").value) if t.has("award") else ""
            num = plain(t.get("number").value) if t.has("number") else ""
            if region and award:
                out.append({"region": region, "award": (f"{num}× " if num and num not in ("1",) else "") + award})
    return out


def mb_tracks(title):
    """MusicBrainz fallback: the release group's earliest official release track list."""
    q = urllib.parse.quote(f'releasegroup:"{title}" AND artist:"Bob Dylan"')
    hdr = {"user-agent": UA, "accept": "application/json"}
    def get(u):
        time.sleep(1.1)
        with urllib.request.urlopen(urllib.request.Request(u, headers=hdr), timeout=60) as r:
            return json.load(r)
    rg = get(f"https://musicbrainz.org/ws/2/release-group/?query={q}&fmt=json&limit=3")
    if not rg.get("release-groups"):
        return [], None
    g = rg["release-groups"][0]
    rels = get(f"https://musicbrainz.org/ws/2/release?release-group={g['id']}&status=official&fmt=json&limit=5")
    if not rels.get("releases"):
        return [], None
    rel = sorted(rels["releases"], key=lambda r: r.get("date") or "9999")[0]
    full = get(f"https://musicbrainz.org/ws/2/release/{rel['id']}?inc=recordings&fmt=json")
    out = []
    for i, m in enumerate(full.get("media", []), 1):
        side = m.get("title") or (f"Disc {i}" if len(full["media"]) > 1 else "")
        for tr in m.get("tracks", []):
            ms = tr.get("length")
            out.append({"side": side, "n": int(tr.get("position") or 0), "title": tr["title"], "writer": "",
                        "length": f"{ms // 60000}:{(ms // 1000) % 60:02d}" if ms else ""})
    return out, {"release": rel["id"], "url": f"https://musicbrainz.org/release/{rel['id']}", "released": rel.get("date", "")}


n_ok = 0
for a in ALBUMS:
    slug = a["s"]
    title = TITLES.get(slug)
    rec = {"s": slug, "t": a["t"], "y": a["y"]}
    if title:
        d = wiki(title)
        code = mw.parse(d["wikitext"])
        box = infobox(code)
        rec.update({
            "released": ib(box, "released", "release_date"),
            "recorded": ib(box, "recorded"),
            "studios": split_list(ib(box, "studio")),
            "venues": split_list(ib(box, "venue")),
            "producers": split_list(ib(box, "producer")),
            "label": ib(box, "label"),
            "length": ib(box, "length"),
            "genres": split_list(ib(box, "genre")),
            "personnel": personnel(code),
            "tracks": tracks(code),
            "charts": charts(code),
            "certs": certs(code),
            "wiki": {"title": d["title"], "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(d["title"].replace(" ", "_")), "revid": d.get("revid")},
        })
    if not rec.get("tracks"):
        try:
            tr, mb = mb_tracks(a["t"].split(" – ")[0].replace("’", "'"))
            if tr:
                rec["tracks"] = tr
                rec["mb"] = mb
        except Exception as e:
            print("  musicbrainz failed", slug, e, file=sys.stderr)
    (OUT / f"{slug}.json").write_text(json.dumps(rec, ensure_ascii=False, separators=(",", ":")))
    n_ok += 1
    print(f"{slug}: {len(rec.get('tracks', []))} tracks, {len(rec.get('personnel', []))} people, {len(rec.get('charts', []))} charts")
print(n_ok, "albums written")
