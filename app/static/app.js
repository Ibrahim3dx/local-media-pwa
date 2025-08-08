async function getJSON(url){ const r = await fetch(url); if(!r.ok) throw new Error(await r.text()); return r.json(); }

async function load(){
  try{
    const h = await getJSON('/api/health');
    document.getElementById('serverInfo').textContent = ` · Root: ${h.root}`;
  }catch(e){ console.error(e); }
  search();
}

async function search(){
  const q = document.getElementById('q').value.trim();
  const t = document.getElementById('type').value;
  const params = new URLSearchParams();
  if(q) params.set('q', q);
  if(t) params.set('type', t);
  const res = await getJSON('/api/items?' + params.toString());
  const grid = document.getElementById('grid'); grid.innerHTML = '';
  for(const it of res.items){
    const card = document.createElement('div'); card.className = 'card';
    const name = it.path.split(/[/\\]/).pop();
    if(it.type==='video'){
      const v = document.createElement('video'); v.controls = true; v.src = `/api/stream/${it.id}`; card.appendChild(v);
    }else if(it.type==='audio'){
      const a = document.createElement('audio'); a.controls = true; a.src = `/api/stream/${it.id}`; card.appendChild(a);
    }else{
      const img = document.createElement('img'); img.loading='lazy'; img.src = `/api/stream/${it.id}`; card.appendChild(img);
    }
    const p = document.createElement('div'); p.textContent = name; p.className='muted'; card.appendChild(p);
    grid.appendChild(card);
  }
}

document.getElementById('searchBtn').addEventListener('click', search);
document.getElementById('q').addEventListener('keydown', (e)=>{ if(e.key==='Enter') search(); });
document.getElementById('type').addEventListener('change', search);

load();
