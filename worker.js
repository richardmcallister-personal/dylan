// Dylan fan site Worker: serves ./site and proxies setlist.fm with a KV cache.
// Secrets (Worker settings, never in the repo): SETLISTFM_KEY, ANTHROPIC_API_KEY.
// KV: DYLAN_CACHE.

const MBID = "72c536dc-7137-4477-a521-567eeb840fa8"; // Bob Dylan on MusicBrainz / setlist.fm
const SFM = "https://api.setlist.fm/rest/1.0";
const UA = "dylan-fansite/1.0 (+https://github.com/richardmcallister-personal/dylan)";

const json = (data, status = 200, maxAge = 0) =>
  new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": maxAge ? `public, max-age=${maxAge}` : "no-store",
    },
  });

// One setlist.fm GET, cached in KV for `ttl` seconds. Returns parsed JSON or throws {status}.
async function sfm(env, path, ttl) {
  const key = "sfm:v1:" + path;
  if (env.DYLAN_CACHE) {
    const hit = await env.DYLAN_CACHE.get(key, "json");
    if (hit) return hit;
  }
  if (!env.SETLISTFM_KEY) throw { status: 503, msg: "SETLISTFM_KEY not set" };
  const r = await fetch(SFM + path, {
    headers: { "x-api-key": env.SETLISTFM_KEY, accept: "application/json", "accept-language": "en", "user-agent": UA },
  });
  if (r.status === 404) {
    const empty = { setlist: [], total: 0, page: 0, itemsPerPage: 20 };
    return empty;
  }
  if (!r.ok) throw { status: r.status, msg: "setlist.fm " + r.status };
  const data = await r.json();
  if (env.DYLAN_CACHE) await env.DYLAN_CACHE.put(key, JSON.stringify(data), { expirationTtl: Math.max(60, ttl) });
  return data;
}

// Compact form of a setlist.fm setlist: what the pages need, nothing more.
function slim(s) {
  const [dd, mm, yyyy] = (s.eventDate || "").split("-");
  const v = s.venue || {};
  const city = v.city || {};
  const sets = ((s.sets || {}).set || []).map((set) => ({
    e: set.encore || 0,
    n: set.name || "",
    s: (set.song || [])
      .filter((x) => x.name && !x.tape)
      .map((x) => {
        const o = { n: x.name };
        if (x.cover && x.cover.name) o.c = x.cover.name;
        if (x.info) o.i = x.info;
        if (x.with && x.with.name) o.w = x.with.name;
        return o;
      }),
  }));
  return {
    id: s.id,
    d: `${yyyy}-${mm}-${dd}`,
    v: v.name || "",
    c: city.name || "",
    st: city.stateCode || "",
    cc: (city.country || {}).code || "",
    cn: (city.country || {}).name || "",
    t: (s.tour || {}).name || "",
    u: s.url || "",
    sets,
  };
}

async function health(env) {
  const out = { setlistfm: { ok: false }, anthropic: { ok: false }, kv: !!env.DYLAN_CACHE };
  if (!env.SETLISTFM_KEY) out.setlistfm.error = "secret SETLISTFM_KEY not set";
  else {
    try {
      const r = await fetch(`${SFM}/artist/${MBID}`, {
        headers: { "x-api-key": env.SETLISTFM_KEY, accept: "application/json", "user-agent": UA },
      });
      out.setlistfm.status = r.status;
      out.setlistfm.ok = r.ok;
      if (r.ok) out.setlistfm.artist = (await r.json()).name;
    } catch (e) {
      out.setlistfm.error = String(e);
    }
  }
  if (!env.ANTHROPIC_API_KEY) out.anthropic.error = "secret ANTHROPIC_API_KEY not set";
  else {
    try {
      const r = await fetch("https://api.anthropic.com/v1/models?limit=1", {
        headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01" },
      });
      out.anthropic.status = r.status;
      out.anthropic.ok = r.ok;
    } catch (e) {
      out.anthropic.error = String(e);
    }
  }
  return json(out);
}

async function api(url, env) {
  const p = url.pathname;
  try {
    // Newest shows (page 1), slimmed. Used by the home and concerts pages.
    if (p === "/api/latest") {
      const d = await sfm(env, `/artist/${MBID}/setlists?p=1`, 1800);
      return json({ total: d.total, shows: (d.setlist || []).map(slim) }, 200, 600);
    }
    // One page of the full history, slimmed. Used by tools/build_setlists.py.
    if (p === "/api/setlists") {
      const page = Math.max(1, Math.min(500, parseInt(url.searchParams.get("p") || "1", 10) || 1));
      const d = await sfm(env, `/artist/${MBID}/setlists?p=${page}`, page === 1 ? 1800 : 86400 * 3);
      return json({ total: d.total, page: d.page, per: d.itemsPerPage, shows: (d.setlist || []).map(slim) }, 200, 600);
    }
    // One show by setlist.fm id.
    if (p === "/api/setlist") {
      const id = (url.searchParams.get("id") || "").replace(/[^a-z0-9]/gi, "");
      if (!id) return json({ error: "id required" }, 400);
      const d = await sfm(env, `/setlist/${id}`, 86400 * 7);
      if (!d.id) return json({ error: "not found" }, 404);
      return json(slim(d), 200, 3600);
    }
    return json({ error: "not found" }, 404);
  } catch (e) {
    return json({ error: e.msg || String(e) }, e.status || 500);
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method !== "GET" && request.method !== "HEAD") return new Response("Method not allowed", { status: 405 });
    if (url.pathname === "/health") return health(env);
    if (url.pathname.startsWith("/api/")) return api(url, env);
    return env.ASSETS.fetch(request);
  },
};
