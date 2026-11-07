/* bobdylan.app — shared shell and helpers (layout from manutd.wiki). */
(function () {
  const D = (window.D = {});
  const NAV = [
    ["home", "/", "Home", '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>'],
    ["albums", "/albums/", "Albums", '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>'],
    ["songs", "/songs/", "Songs", '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>'],
    ["concerts", "/concerts/", "Shows", '<path d="M4 20h16M6 20V9l6-5 6 5v11"/><path d="M10 20v-5h4v5"/>'],
    ["journeys", "/journeys/", "Journeys", '<path d="M3 17c4 0 4-10 9-10s5 10 9 10"/><circle cx="3" cy="17" r="1.5"/><circle cx="21" cy="17" r="1.5"/>'],
  ];
  const archiveNav = [["books", "/books/", "Books"], ["influences", "/influences/", "Influences"], ["timeline", "/timeline/", "Timeline"]];
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
  // Spotify player: a tap-to-load facade (no Spotify cookies or weight until the visitor asks for it).
  D.spId = (url) => ((url || "").match(/open\.spotify\.com\/(album|track)\/([A-Za-z0-9]+)/) || []).slice(1);
  D.player = (kind, id, label) =>
    `<div class="player ${kind}" data-kind="${kind}" data-id="${id}"><button type="button" class="play" aria-label="Load Spotify player: ${D.esc(label)}">` +
    `<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="currentColor"/><path d="M9.5 7.5v9l7-4.5z" fill="var(--paper)"/></svg>` +
    `<span><b>Play ${kind === "album" ? "the album" : "the song"}</b><small>${D.esc(label)} · loads Spotify's player</small></span></button></div>`;
  document.addEventListener("click", (e) => {
    const b = e.target.closest(".player .play");
    if (!b) return;
    const w = b.parentElement;
    w.innerHTML = `<iframe title="Spotify player" src="https://open.spotify.com/embed/${w.dataset.kind}/${w.dataset.id}?utm_source=generator" width="100%" height="${w.dataset.kind === "album" ? 352 : 152}" frameborder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>`;
    w.classList.add("on");
  });
  // Tour dates (from bobdylan.com via tools/build_tour.py) as gig rows with ticket buttons.
  D.tour = async () => {
    const t = await D.get("/data/tour.json").catch(() => ({ dates: [] }));
    const today = D.today();
    return t.dates.filter((x) => x.d >= today);
  };
  D.gig = (x) => {
    const [y, m, d] = x.d.split("-").map(Number);
    const wd = new Date(Date.UTC(y, m - 1, d)).toLocaleDateString("en-GB", { weekday: "short", timeZone: "UTC" });
    return `<li><div class="d"><b>${d}</b>${MON[m - 1]} ${y}<small>${wd}</small></div>
      <div class="o"><a href="${x.page}" target="_blank" rel="noopener">${D.esc(x.venue)}</a><small>${D.esc(x.city)}</small></div>
      <div class="a">${x.tickets ? `<a class="btn pri sm" href="${x.tickets}" target="_blank" rel="noopener">Tickets</a>` : ""}${x.vip ? `<a class="btn sm" href="${x.vip}" target="_blank" rel="noopener">VIP</a>` : ""}${x.presale ? `<a class="btn sm" href="${x.presale}" target="_blank" rel="noopener">Pre-sale</a>` : ""}</div></li>`;
  };
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
    const nav = [...NAV, ...archiveNav].map(([k, href, label]) => `<a class="${archiveNav.some(([id]) => id === k) ? "archive-link" : "main-link"}" href="${href}"${k === page ? ' aria-current="page"' : ""}>${label}</a>`).join("");
    const tabs = NAV.map(([k, href, label, p]) => `<a href="${href}"${k === page ? ' aria-current="page"' : ""}>${ic(p)}<span>${label}</span></a>`).join("");
    document.body.insertAdjacentHTML(
      "afterbegin",
      `<a class="skip" href="#main">Skip to content</a>
      <div class="mast"><div class="wrap">
        <header class="mu"><a class="brand" href="/" aria-label="Bob Dylan home"><img class="emblem" src="/assets/dylan-eye.png" width="344" height="344" alt=""><img class="wordmark" src="/assets/bob-dylan.png" width="604" height="79" alt="Bob Dylan"></a></header>
        <nav class="munav" aria-label="Main">${nav}<div class="musearch" role="search"><input type="search" id="q-site" placeholder="Search songs and albums" aria-label="Search songs and albums" autocomplete="off"><div class="hits" hidden></div></div></nav>
      </div></div>`
    );
    document.body.insertAdjacentHTML(
      "beforeend",
      `<nav class="tabbar" aria-label="Main">${tabs}</nav>
      <footer class="mu wrap">
        <div>Setlists from <a href="https://www.setlist.fm/setlists/bob-dylan-23d6b8d3.html" rel="noopener">setlist.fm</a>. Tour dates and tickets from <a href="https://www.bobdylan.com/on-tour/" rel="noopener">bobdylan.com</a>.</div>
        <div class="theme" role="group" aria-label="Theme"><span>Theme</span><button type="button" data-t="auto">Auto</button><button type="button" data-t="light">Light</button><button type="button" data-t="dark">Dark</button></div>
      </footer>`
    );
    const t = curTheme();
    document.querySelectorAll(".theme button").forEach((b) => {
      b.setAttribute("aria-pressed", b.dataset.t === t);
      b.addEventListener("click", () => D.setTheme(b.dataset.t));
    });
    search();
  };

  // Site search: songs and albums, built on first focus.
  function search() {
    const inp = document.getElementById("q-site"), box = inp.nextElementSibling;
    let idx = null, sel = -1, items = [];
    const norm = (s) => s.normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[’']/g, "");
    const load = async () => {
      if (idx) return idx;
      const [songs, albums] = await Promise.all([D.get("/data/songs.json"), D.albums()]);
      idx = albums.map((a) => ({ k: "a", n: a.t, t: norm(a.t), h: "/albums/?a=" + a.s, sub: a.y + " · " + a.c.map((c) => D.CAT[c]).join(", "), a, w: 1000 }))
        .concat(songs.map((s) => ({ k: "s", n: s.n, t: norm(s.n), h: "/song/?s=" + s.s, sub: s.k + " times live" + (s.c ? " · " + s.c + " cover" : ""), w: s.k })));
      return idx;
    };
    const draw = () => {
      if (!inp.value.trim()) { box.hidden = true; return; }
      box.hidden = false;
      box.innerHTML = items.length
        ? items.map((x, i) => `<a href="${x.h}"${i === sel ? ' class="sel"' : ""}>${x.k === "a" ? D.cover(x.a, 44, 'alt=""') : '<span class="ic">Song</span>'}<span><b>${D.esc(x.n)}</b><small>${D.esc(x.sub)}</small></span></a>`).join("")
        : `<div class="none">Nothing matches “${D.esc(inp.value)}”.</div>`;
    };
    inp.addEventListener("focus", load);
    inp.addEventListener("input", async () => {
      const q = norm(inp.value.trim());
      const all = await load();
      items = q ? all.filter((x) => x.t.includes(q)).sort((a, b) => (b.t.startsWith(q) - a.t.startsWith(q)) || b.w - a.w).slice(0, 8) : [];
      sel = -1; draw();
    });
    inp.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); sel = Math.max(-1, Math.min(items.length - 1, sel + (e.key === "ArrowDown" ? 1 : -1))); draw(); }
      else if (e.key === "Enter" && items.length) { location.href = items[Math.max(0, sel)].h; }
      else if (e.key === "Escape") { inp.value = ""; box.hidden = true; inp.blur(); }
    });
    document.addEventListener("click", (e) => { if (!e.target.closest(".musearch")) box.hidden = true; });
  }

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
