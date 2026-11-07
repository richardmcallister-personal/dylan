(async function () {
  const books = await D.get("/data/books.json");
  const query = document.querySelector("#search-books");
  query.value = D.qs("q") || "";
  const category = document.querySelector("#category");
  const format = document.querySelector("#format");
  const grid = document.querySelector("#catalog");
  const labels = {print:"Print", ebook:"E-book", audio:"Audiobook"};
  const normalize = text => text.normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/['’]/g,"");
  for (const name of [...new Set(books.map(b => b.category))].sort()) category.add(new Option(name,name));
  function render() {
    const term = normalize(query.value.trim());
    const list = books.filter(b => (!category.value || b.category === category.value) &&
      (!format.value || b[format.value]) && normalize([b.title,b.subtitle,b.author].filter(Boolean).join(" ")).includes(term));
    document.querySelector("#count").textContent = list.length+" of "+books.length+" books";
    grid.innerHTML = list.map(b => {
      const links = Object.entries(labels).filter(([k]) => b[k]).map(([k,label]) =>
        '<a href="'+D.esc(b[k])+'" aria-label="'+D.esc(label+' edition of '+b.title)+'">'+label+'</a>').join("");
      return '<article class="book-card"><div class="book-art"><img src="'+D.esc(b.cover)+'" alt="'+D.esc(b.title)+' cover" loading="lazy"></div>'+
        '<small class="muted">'+D.esc(b.category)+'</small><h2>'+D.esc(b.title)+'</h2>'+(b.subtitle?'<p class="small muted">'+D.esc(b.subtitle)+'</p>':'')+'<p>'+D.esc(b.author)+'</p>'+
        '<p class="small muted">'+(b.original?'First published '+b.original+' · ':'')+'Listed edition · '+D.esc(b.date)+'</p>'+
        '<div class="book-actions">'+links+'</div><a class="small" href="'+D.esc(b.source)+'">Edition details</a></article>';
    }).join("") || "<p>No matching books. Try another title, author, or format.</p>";
  }
  grid.addEventListener("error", e => {
    if(e.target.tagName === "IMG") e.target.parentElement.textContent = e.target.alt.replace(/ cover$/, "");
  },true);
  query.addEventListener("input",render);
  category.addEventListener("change",render);
  format.addEventListener("change",render);
  render();
  document.querySelector("#status").hidden = true;
})().catch(() => {document.querySelector("#status").textContent="The bookshelf could not load. Please reload the page.";});
