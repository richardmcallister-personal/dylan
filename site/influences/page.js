(async function () {
  const artists = await D.get("/data/influences.json");
  const groups = [["roots","Artists who influenced Dylan"],["legacy","Artists Dylan influenced"]];
  document.querySelector("#connections").innerHTML = groups.map(([id,title]) =>
    '<section class="influence-group" id="'+id+'"><h2>'+title+'</h2><div class="influence-list">'+
    artists.filter(a => a.direction === title).map(a =>
      '<article id="artist-'+D.slug(a.name)+'"><div class="artist-heading"><a href="'+D.esc(a.spotify)+'" tabindex="-1" aria-hidden="true"><img src="'+D.esc(a.image)+'" alt="" width="116" height="116" loading="lazy"></a><div><h3>'+D.esc(a.name)+'</h3><a href="'+D.esc(a.spotify)+'" aria-label="'+D.esc('Listen to '+a.name+' on Spotify')+'">Listen on Spotify</a></div></div><p>'+D.esc(a.note)+'</p><a href="'+D.esc(a.source)+'">'+D.esc(new URL(a.source).hostname.replace(/^www\./,""))+'</a></article>').join("")+
    '</div></section>').join("");
  document.querySelector("#status").hidden = true;
  if (location.hash) document.getElementById(location.hash.slice(1))?.scrollIntoView();
})().catch(() => {document.querySelector("#status").textContent="The influences could not load. Please reload the page.";});
