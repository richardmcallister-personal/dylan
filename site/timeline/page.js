(async function () {
  const [albums, dates, index, milestones] = await Promise.all([D.albums(),D.get("/data/album-dates.json"),D.get("/data/index.json"),D.get("/data/milestones.json")]);
  const releases = albums.map(a => ({
    date:dates[a.s]?.date || String(a.y), kind:"Album", title:a.t,
    link:"/albums/?a="+encodeURIComponent(a.s), source:dates[a.s]?.source || a.o
  }));
  const years = [...new Set([...Object.keys(index.years), ...[...milestones,...releases].map(e => e.date.slice(0,4))])].sort();
  const yearSelect = document.querySelector("#year"), kindSelect = document.querySelector("#kind"), list = document.querySelector("#years-list");
  for (const year of years) yearSelect.add(new Option(year,year));
  function events(year,kind) {
    const rows = kind === "Concerts" ? [] : kind === "Albums" ? releases : kind === "Awards" ? milestones.filter(e => e.kind === kind) :
      kind === "Milestones" ? milestones : [...milestones,...releases];
    return rows.filter(e => e.date.startsWith(year));
  }
  function readable(date) {
    if(date.length === 4) return date;
    const full = date.length === 7;
    return new Intl.DateTimeFormat("en-GB",{year:"numeric",month:"short",day:full?undefined:"numeric",timeZone:"UTC"}).format(new Date((full?date+"-01":date)+"T00:00:00Z"));
  }
  function row(e) {
    const title=e.link ? '<a href="'+D.esc(e.link)+'">'+D.esc(e.title)+'</a>' : D.esc(e.title);
    return '<article class="timeline-event"><time datetime="'+D.esc(e.date)+'">'+readable(e.date)+'</time><div><small class="muted">'+D.esc(e.kind)+'</small><h3>'+title+'</h3>'+
      (e.note?'<p>'+D.esc(e.note)+'</p>':'')+(e.source?'<a class="small" href="'+D.esc(e.source)+'">Source</a>':'')+'</div></article>';
  }
  function render() {
    const kind=kindSelect.value, showConcerts=!kind || kind==="Concerts";
    let total=0;
    list.replaceChildren();
    for(const year of years.filter(y=>!yearSelect.value || yearSelect.value===y)){
      const fixed=events(year,kind);
      const concerts=showConcerts ? index.years[year] || 0 : 0;
      const count=fixed.length+concerts;
      if(!count) continue;
      total+=count;
      const group=document.createElement("details");
      group.className="timeline-year";
      group.innerHTML='<summary>'+year+'<small>'+count+' '+(count===1?'event':'events')+'</small></summary><div></div>';
      const content=group.lastElementChild;
      let populated=false;
      async function expand() {
        if(!group.open || populated) return;
        populated=true;
        content.textContent="Loading…";
        try {
          const shows=concerts ? await D.get("/data/years/"+year+".json") : [];
          const rows=[...fixed,...shows.map(s=>({date:s.d,kind:"Concert",title:s.v,note:D.place(s),link:"/concert/?id="+encodeURIComponent(s.id)}))];
          content.innerHTML=rows.sort((a,b)=>a.date.localeCompare(b.date)||a.title.localeCompare(b.title)).map(row).join("");
        } catch {
          populated=false;
          content.innerHTML=fixed.map(row).join("")+'<p>Concert records could not load. <a href="/concerts/?y='+year+'">Open the concert archive</a>.</p>';
        }
      }
      group.addEventListener("toggle",expand);
      list.append(group);
      if(yearSelect.value || list.childElementCount===1) group.open=true;
    }
    document.querySelector("#count").textContent=total+" "+(total===1?"event":"events");
    if(!total) list.textContent="No events match this selection.";
  }
  if(years.includes(D.qs("y"))) yearSelect.value=D.qs("y");
  yearSelect.addEventListener("change",render);kindSelect.addEventListener("change",render);render();
  document.querySelector("#status").hidden=true;
})().catch(() => {document.querySelector("#status").textContent="The timeline could not load. Please reload the page.";});
