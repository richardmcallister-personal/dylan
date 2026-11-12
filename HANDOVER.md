# bobdylan.app — handover (7 Nov 2026)

Start a new chat with the repo `richardmcallister-personal/dylan` attached. Read `CLAUDE.md` first; this
file only says where things stand.

## State of the site (v1, live on bobdylan.app)

- 7 Nov afternoon: manutd.wiki layout; Bob Dylan wordmark in the masthead; Center logo and exterior photo on the homepage; black eye emblem in the masthead, favicon and app icons; site search; tour dates with Tickets / VIP / pre-sale links from
  bobdylan.com (`tools/build_tour.py`, 19 dates at build) on home, Shows and upcoming setlist pages; Spotify
  players: albums now (tap-to-load, in the album dialog, deep link `/albums/?a=<slug>`), songs once Spotify keys are
  added as Worker secrets.

- Worker `dylan` on bobdylan.app (www redirects to the apex) and dylan.richardmcallister.workers.dev.
  `/health`: setlist.fm OK, Anthropic OK, KV bound.
- **Home:** hero with live counts and a studio-album cover strip; latest show with its first songs (live from
  setlist.fm); upcoming dates; Like a Rolling Stone feature; On this day; top 10 most played; journey cards.
- **Albums** (`/albums/`): cover wall of all 82 official-catalogue albums, filters (studio 40, live 13,
  compilations 10, Bootleg Series 19 incl. edition variants), oldest/newest, decade headers, dialog with
  official page + Spotify (exact edition vs "related edition" vs search, from the kit's matching notes).
- **Journeys** (`/journeys/`, `data/journeys.json`): six routes — acoustic storyteller, going electric,
  basement/barn/Nashville, Blood on the Tracks era, gospel years, late masterpieces — each 4–5 albums with a
  note and "start with" songs (linked to song pages with live counts, or marked "not played live").
- **Songs** (`/songs/`): 800 songs from the setlists, search, his songs / covers, sort by plays, A–Z, recent.
- **Song page** (`/song/?s=`): plays, rank, first/latest show, years active and peak, bars per year, every
  performance by year. Curated "One song, many lives" timeline where `data/lives/<slug>.json` exists and the
  slug is listed in `data/lives/index.json` — so far only `like-a-rolling-stone` (7 lives + covers by others).
- **Shows** (`/concerts/`): year picker, shows per year, upcoming dates (live). **Setlist** (`/concert/?id=`):
  live from the Worker, sets/encores, covers and guests marked, "first performance" flag, setlist.fm credit.
- Data built 7 Nov 2026: 4164 shows (4039 with setlists), 52 countries, 800 songs, 2 upcoming.

## Known gaps

- **Missing tours:** 1974 (with the Band), most of 1986–87 (Tom Petty / Grateful Dead era), and other
  co-billed shows are not under Bob Dylan's setlist.fm artist listing, so they're absent. Not yet verified which
  setlist.fm artists hold them — check with the setlist.fm search API (add a Worker route), then extend the
  builder to merge them. Both the Shows page and song pages say these years are missing.
- English only (manutd.wiki's i18n engine not ported).
- Data only refreshes when `tools/build_setlists.py` is run; home/Shows/setlist pages read latest shows live.
- The resource kit's SPOTIFY-DISCOVERY.md / ALBUM-CATALOG.md are not used yet.

## Next candidates

1. Weekly scheduled task: run `build_setlists.py` and `build_tour.py` (tour weekly at least — ticket links
   change), commit the JSON, push.
1b. Spotify keys from Richard (developer.spotify.com app → `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET` secrets);
   `/health` shows spotify ok when they work.
2. Fill the missing tours (see above).
3. More "many lives" songs: Tangled Up in Blue (rewritten lyrics across versions — describe, never quote),
   All Along the Watchtower, Mr. Tambourine Man, Blowin' in the Wind.
4. Ask the archive (Anthropic key is already on the Worker): same pattern as manutd.wiki's `/ask`, built on
   the site's JSON, with a hard rule never to quote lyrics.
5. "Were you there?" — personal show memories (KV), and Richard's own shows.
6. Home Screen icons/splash for iOS like manutd.wiki; tour alerts via Web Push.

## How to refresh the data

```
python3 tools/build_setlists.py          # ~3 min, 209 pages through the Worker
git add site/data && git commit … && git push
```
Re-import the kit (after Richard adds covers): `python3 tools/import_kit.py <path-to-dylan-resource-kit>`.

## 8 Nov 2026 — album pages

- Album pages for all 82 albums (facts, musicians, studios, charts, certifications, cover story, influence,
  tracks with live counts and official lyric links, Spotify album player, prev/next). Home hero: eye emblem on the
  right, album carousel below. Spotify keys added by Richard; `/health` shows spotify ok, song players live.
- Known gaps: no Wikipedia article for Live 1962–1966 or Through the Open Window (MusicBrainz track lists only,
  first release's edition); several albums have no chart table in their article (Saved, Shot of Love, Oh Mercy,
  Under the Red Sky, etc.); personnel missing for most compilations and some archive sets.
- Re-run: `python3 tools/build_albums.py` (reads Wikipedia through bobdylan.app/api/wiki, cached in KV 7 days).

## 8 Nov 2026 — gallery

- `/gallery/` with Richard's 300 photos (1963–2023), in date order, filter by decade/year/country/place, lightbox.
  238 photos matched to one setlist.fm show (link to its setlist); 54 to a city with several shows that year (link
  to that year); 8 unmatched (mostly years missing from setlist.fm, e.g. 1974/1986–87).
- No photographer credits yet — the photos came without metadata. Add a credits field to gallery.json when known.

## 12 Nov 2026 — song genealogy

- `/genealogy/` (masthead, footer, home feature). 15 songs traced: Blowin' in the Wind, Don't Think Twice, Masters of
  War, Girl from the North Country, Mr. Tambourine Man, Like a Rolling Stone, Desolation Row, Visions of Johanna,
  Simple Twist of Fate, I Shall Be Released, Knockin' on Heaven's Door, Tangled Up in Blue, All Along the Watchtower,
  Every Grain of Sand, Make You Feel My Love. Every song page now has a computed stage history.
- Next candidates: It's Alright Ma, Just Like a Woman, Ballad of a Thin Man, Highway 61 Revisited, Shelter from the
  Storm, Gotta Serve Somebody, Things Have Changed, Forever Young.
