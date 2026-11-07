/* Dylan Notes — shared shell and helpers. */
(function () {
  const D = (window.D = {});
  D.NAME = "Dylan Notes";

  const NAV = [
    ["home", "/", "Home", '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>'],
    ["albums", "/albums/", "Albums", '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>'],
    ["songs", "/songs/", "Songs", '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>'],
    ["concerts", "/concerts/", "Shows", '<path d="M4 20h16M6 20V9l6-5 6 5v11"/><path d="M10 20v-5h4v5"/>'],
    ["journeys", "/journeys/", "Journeys", '<path d="M3 17c4 0 4-10 9-10s5 10 9 10"/><circle cx="3" cy="17" r="1.5"/><circle cx="21" cy="17" r="1.5"/>'],
  ];
  const ic = (p) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${p}</svg>`;

  D.esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  D.slug = (s) =>
    String(s).normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/['’`]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "song";
  const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  D.date = (iso, long) => {
    if (!iso) return "";
    const [y, m, d] = iso.split("-").map(Number);
    if (long) {
      const wd = new Date(Date.UTC(y, m - 1, d)).toLocaleDateString("en-GB", { weekday: "short", timeZone: "UTC" });
      return `${wd} ${d} ${MON[m - 1]} ${y}`;
    }
    return `${d} ${MON[m - 1]} ${y}`;
  };
  D.today = () => {
    const t = new Date();
    return `${t.getFullYear()}-${String(t.getMonth() + 1).padStart(2, "0")}-${String(t.getDate()).padStart(2, "0")}`;
  };
  D.place = (s) => [s.c, s.cc === "US" && s.st && isNaN(+s.st) ? s.st : s.cn || s.cc].filter(Boolean).join(", ");

  const memo = {};
  D.get = (url) =>
    (memo[url] =
      memo[url] ||
      fetch(url).then((r) => {
        if (!r.ok) throw new Error(url + " " + r.status);
        return r.json();
      }));
  D.albums = () => D.get("/data/albums.json");
  D.album = async (slug) => (await D.albums()).find((a) => a.s === slug);
  D.CAT = { studio: "Studio", live: "Live", comp: "Compilation", bootleg: "Bootleg Series" };
  D.cover = (a, px = 160, extra = "") =>
    `<img src="/covers/${a.s}.webp" alt="${D.esc(a.t)} cover" width="${px}" height="${px}" loading="lazy" decoding="async" ${extra}>`;
  D.spotify = (a) =>
    a.sp && a.spx
      ? `<a class="btn pri" href="${a.sp}" target="_blank" rel="noopener">Listen on Spotify</a>`
      : a.sp
      ? `<a class="btn" href="${a.sp}" target="_blank" rel="noopener">Spotify (related edition)</a>`
      : `<a class="btn" href="${a.ss}" target="_blank" rel="noopener">Search Spotify</a>`;
  D.qs = (k) => new URLSearchParams(location.search).get(k);

  // Theme: auto / light / dark, remembered per browser.
  const THEME_KEY = "dn_theme";
  D.setTheme = (t) => {
    try {
      t === "auto" ? localStorage.removeItem(THEME_KEY) : localStorage.setItem(THEME_KEY, t);
    } catch (e) {}
    t === "auto" ? document.documentElement.removeAttribute("data-theme") : document.documentElement.setAttribute("data-theme", t);
    document.querySelectorAll(".theme button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.t === t));
  };
  const curTheme = () => {
    try {
      return localStorage.getItem(THEME_KEY) || "auto";
    } catch (e) {
      return "auto";
    }
  };

  D.shell = (page) => {
    const nav = NAV.map(([k, href, label]) => `<a href="${href}"${k === page ? ' aria-current="page"' : ""}>${label}</a>`).join("");
    const tabs = NAV.map(([k, href, label, p]) => `<a href="${href}"${k === page ? ' aria-current="page"' : ""}>${ic(p)}<span>${label}</span></a>`).join("");
    document.body.insertAdjacentHTML(
      "afterbegin",
      `<a class="skip" href="#main">Skip to content</a>
      <header class="mast"><div class="in">
        <a class="brand" href="/" aria-label="${D.NAME} home"><b>Dylan<i>.</i>Notes</b><small>Unofficial fan site</small></a>
        <nav class="nav" aria-label="Main">${nav}</nav>
      </div></header>`
    );
    document.body.insertAdjacentHTML(
      "beforeend",
      `<nav class="tabbar" aria-label="Main">${tabs}</nav>
      <footer class="foot"><div class="in">
        <div><b>${D.NAME}</b> is an unofficial fan site. It is not connected with Bob Dylan, his management, Columbia/Sony Music or the Bob Dylan Center.
        For the official site, lyrics and tour dates, visit <a href="https://www.bobdylan.com/" rel="noopener">bobdylan.com</a>.</div>
        <div>Concert and setlist data from <a href="https://www.setlist.fm/setlists/bob-dylan-23d6b8d3.html" rel="noopener">setlist.fm</a>, compiled by its users.
        Album artwork © the respective rights holders, shown small to identify each record, with links to its official page.</div>
        <div class="theme" role="group" aria-label="Theme">Theme
          <button type="button" data-t="auto">Auto</button><button type="button" data-t="light">Light</button><button type="button" data-t="dark">Dark</button>
        </div>
      </div></footer>`
    );
    const t = curTheme();
    document.querySelectorAll(".theme button").forEach((b) => {
      b.setAttribute("aria-pressed", b.dataset.t === t);
      b.addEventListener("click", () => D.setTheme(b.dataset.t));
    });
  };

  // Year bar chart: {yyyy: n} → bars from first..last year (or given range).
  D.bars = (byYear, from, to, hot) => {
    const ys = Object.keys(byYear).map(Number);
    if (!ys.length) return "";
    from = from || Math.min(...ys);
    to = to || Math.max(...ys);
    const max = Math.max(...Object.values(byYear));
    let h = "";
    for (let y = from; y <= to; y++) {
      const n = byYear[y] || 0;
      h += `<i class="${hot && hot(y, n) ? "hot" : ""}" style="height:${n ? Math.max(3, (n / max) * 100) : 0}%" title="${y}: ${n}"></i>`;
    }
    return `<div class="bars" role="img" aria-label="Performances per year, ${from} to ${to}">${h}</div><div class="bars-x"><span>${from}</span><span>${Math.round((from + to) / 2)}</span><span>${to}</span></div>`;
  };
})();
