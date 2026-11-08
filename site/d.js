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
      }).catch(error => { delete memo[url]; throw error; }));
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

  // Site footer (manutd.wiki pattern): brand and sources, then the sections and official links.
  function siteFooter() {
    const col = (h, links) => `<div class="fcol"><h2>${h}</h2><ul>${links.map(([href, label]) => `<li><a href="${href}"${/^https?:/.test(href) ? ' target="_blank" rel="noopener"' : ""}>${label}</a></li>`).join("")}</ul></div>`;
    return `<div class="sitefoot">
      <div class="fbrand"><a class="fname" href="/"><span>Bob Dylan</span></a><small>Fan site</small>
        <p>The records, the songs and every show on record since 1956, kept by a fan.</p></div>
      <div class="fcols">
        ${col("Listen", [["/albums/", "Albums"], ["/journeys/", "Listening journeys"], ["/songs/", "Songs"], ["/song/?s=like-a-rolling-stone", "One song, many lives"]])}
        ${col("Live", [["/concerts/#tour", "On tour"], ["/concerts/", "Shows by year"]])}
        ${col("Archive", [["/books/", "Books"], ["/influences/", "Influences"], ["/timeline/", "Timeline"]])}
        ${col("Official", [["https://www.bobdylan.com/", "bobdylan.com"], ["https://www.bobdylan.com/on-tour/", "Tour and tickets"], ["https://www.bobdylancenter.com/", "Bob Dylan Center"], ["https://www.setlist.fm/setlists/bob-dylan-23d6b8d3.html", "setlist.fm"]])}
      </div>
    </div>`;
  }

  D.shell = (page) => {
    const nav = [...NAV, ...archiveNav].map(([k, href, label]) => `<a class="${archiveNav.some(([id]) => id === k) ? "archive-link" : "main-link"}" href="${href}"${k === page ? ' aria-current="page"' : ""}>${label}</a>`).join("");
    const tabs = NAV.map(([k, href, label, p]) => `<a href="${href}"${k === page ? ' aria-current="page"' : ""}>${ic(p)}<span>${label}</span></a>`).join("");
    document.body.insertAdjacentHTML(
      "afterbegin",
      `<a class="skip" href="#main">Skip to content</a>
      <div class="mast"><div class="wrap">
        <header class="mu"><a class="brand" href="/" aria-label="Bob Dylan home"><img class="emblem" src="/assets/dylan-eye.png" width="344" height="344" alt=""><img class="wordmark" src="/assets/bob-dylan.png" width="604" height="79" alt="Bob Dylan"></a></header>
        <nav class="munav" aria-label="Main">${nav}<div class="musearch" role="search"><input type="search" id="q-site" placeholder="Search the archive" aria-label="Search the archive" autocomplete="off"><div class="hits" hidden></div></div></nav>
      </div></div>`
    );
    document.body.insertAdjacentHTML(
      "beforeend",
      `<nav class="tabbar" aria-label="Main">${tabs}</nav>
      <footer class="mu wrap full">${siteFooter()}
        <div class="fnotes">
          <p>This is a fan site, not connected with Bob Dylan, his management or his record label. For the official site, lyrics and news, go to <a href="https://www.bobdylan.com/" rel="noopener">bobdylan.com</a>.</p>
          <p>Setlists from <a href="https://www.setlist.fm/setlists/bob-dylan-23d6b8d3.html" rel="noopener">setlist.fm</a>, compiled by its users. Tour dates and ticket links from <a href="https://www.bobdylan.com/on-tour/" rel="noopener">bobdylan.com</a>. Album artwork © the respective rights holders, shown to identify each record.</p>
          <div class="theme" role="group" aria-label="Theme"><span>Theme</span><button type="button" data-t="auto">Auto</button><button type="button" data-t="light">Light</button><button type="button" data-t="dark">Dark</button></div>
        </div>
      </footer>`
    );
    const t = curTheme();
    document.querySelectorAll(".theme button").forEach((b) => {
      b.setAttribute("aria-pressed", b.dataset.t === t);
      b.addEventListener("click", () => D.setTheme(b.dataset.t));
    });
    search();
  };

  function search() {
    const input = document.getElementById("q-site");
    const box = input.nextElementSibling;
    const normalize = s => String(s).normalize("NFKD").replace(/[\u0300-\u036f]/g,"").toLowerCase().replace(/['’]/g,"").replace(/[^\p{L}\p{N}]+/gu," ").trim();
    let index, selected = -1, visible = [], groups = [], limit = 4, revision = 0;
    async function build() {
      const [songs, albums, books, artists, milestones, days, journeys] = await Promise.all(
        ["songs","albums","books","influences","milestones","otd","journeys"].map(name=>D.get("/data/"+name+".json")));
      const rows = [];
      function add(group,title,detail,url,extra="",weight=0,image="") {
        rows.push({group,title,detail,url,weight,image,key:normalize(title),text:normalize([title,detail,extra].join(" "))});
      }
      for(const a of albums) add("Albums",a.t,a.y+" · "+a.c.map(k=>D.CAT[k]).join(", "),"/album/?a="+a.s,"",0,"/covers/"+a.s+".webp");
      for(const s of songs) add("Songs",s.n,s.k+" times live"+(s.c?" · "+s.c+" cover":""),"/song/?s="+s.s,"",s.k);
      for(const b of books) add("Books",b.title,b.author,"/books/?q="+encodeURIComponent(b.title),[b.category,b.subtitle].filter(Boolean).join(" "));
      for(const a of artists) add("Artists",a.name,a.direction,"/influences/#artist-"+D.slug(a.name),a.note);
      for(const e of milestones) add("Milestones",e.title,e.date+" · "+e.kind,"/timeline/?y="+e.date.slice(0,4)+"#milestone-"+D.slug(e.title),e.note);
      for(const [md,shows] of Object.entries(days)) for(const [year,id,venue,city,country] of shows) {
        const date=year+"-"+md;
        add("Concerts",venue,[city,country,D.date(date)].filter(Boolean).join(" · "),"/concert/?id="+id,date);
      }
      for(const j of journeys) add("Journeys",j.title,j.years,"/journeys/#"+j.id,j.intro);
      return rows;
    }
    function draw() {
      visible=[];
      box.innerHTML=groups.map(([name,rows])=>{
        const links=rows.slice(0,limit).map(r=>{
          visible.push(r);
          return '<a href="'+D.esc(r.url)+'">'+(r.image?'<img src="'+D.esc(r.image)+'" alt="" width="44" height="44">':'')+
            '<span><b>'+D.esc(r.title)+'</b><small>'+D.esc(r.detail)+'</small></span></a>';
        }).join("");
        return '<section><h3>'+name+' <small>'+rows.length+'</small></h3>'+links+'</section>';
      }).join("") || '<div class="none">Nothing matches “'+D.esc(input.value)+'”.</div>';
      if(groups.some(([,rows])=>rows.length>limit)) box.insertAdjacentHTML("beforeend",'<button type="button">Show more matches</button>');
      box.hidden=false;
    }
    async function update() {
      const token=++revision, q=normalize(input.value);
      selected=-1; visible=[]; limit=4;
      if(!q){box.hidden=true;return;}
      try {
        index ||= build().catch(err=>{index=null;throw err;});
        const rows=await index;
        if(token!==revision || document.activeElement!==input) return;
        const words=q.split(" ");
        const hits=rows.filter(r=>words.every(w=>r.text.includes(w)));
        const score=r=>r.key===q?4:r.key.startsWith(q)?3:r.key.includes(q)?2:r.text.includes(q)?1:0;
        hits.sort((a,b)=>score(b)-score(a)||b.weight-a.weight||a.title.localeCompare(b.title));
        const buckets=new Map();
        for(const r of hits){if(!buckets.has(r.group)) buckets.set(r.group,[]);buckets.get(r.group).push(r);}
        groups=[...buckets];draw();
      } catch {
        if(token===revision){box.innerHTML='<div class="none">Search could not load. Try again.</div>';box.hidden=false;}
      }
    }
    input.addEventListener("input",update);
    input.addEventListener("focus",update);
    input.addEventListener("keydown",e=>{
      if(e.key==="Escape"){revision++;input.value="";box.hidden=true;input.blur();return;}
      if(box.hidden || !visible.length)return;
      if(e.key==="Enter"){e.preventDefault();location.href=visible[Math.max(selected,0)].url;return;}
      if(e.key!=="ArrowDown" && e.key!=="ArrowUp") return;
      e.preventDefault();
      selected=Math.max(0,Math.min(visible.length-1,selected+(e.key==="ArrowDown"?1:-1)));
      const links=box.querySelectorAll("a");
      links.forEach((a,i)=>a.classList.toggle("sel",i===selected));
      links[selected].scrollIntoView({block:"nearest"});
    });
    box.addEventListener("click",e=>{if(e.target.closest("button")){const top=box.scrollTop;limit+=10;selected=-1;draw();box.scrollTop=top;}});
    document.addEventListener("click",e=>{if(!e.target.closest(".musearch")){revision++;box.hidden=true;}});
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
