async function getJSON(url){ const r = await fetch(url); if(!r.ok) throw new Error(await r.text()); return r.json(); }
async function sendJSON(url, method, body){ const r = await fetch(url,{method, headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)}); if(!r.ok) throw new Error(await r.text()); return r.json(); }

const statusEl = document.getElementById('status');
const infoEl = document.getElementById('info');
const mediaRootEl = document.getElementById('mediaRoot');
const saveBtn = document.getElementById('saveBtn');
const rescanBtn = document.getElementById('rescanBtn');

async function load(){
  try{
    const health = await getJSON('/api/health');
    infoEl.textContent = JSON.stringify(health, null, 2);
  }catch(e){ infoEl.textContent = 'Health error: ' + e.message; }

  try{
    const cfg = await getJSON('/api/config');
    mediaRootEl.value = cfg.media_root || '';
  }catch(e){
    statusEl.textContent = 'Cannot read config (are you on localhost?): ' + e.message;
  }
}

saveBtn.addEventListener('click', async ()=>{
  const path = mediaRootEl.value.trim();
  if(!path){ statusEl.textContent = 'Please enter a folder path.'; return; }
  statusEl.textContent = 'Saving...';
  try{
    const out = await sendJSON('/api/config','PUT',{media_root: path});
    statusEl.textContent = 'Saved: ' + out.media_root + ' — now rescanning...';
    await fetch('/api/rescan', {method:'POST'});
    statusEl.textContent = 'Rescan complete.';
  }catch(e){
    statusEl.textContent = 'Error: ' + e.message;
  }
});

rescanBtn.addEventListener('click', async ()=>{
  statusEl.textContent = 'Rescanning...';
  try{
    const out = await fetch('/api/rescan', {method:'POST'}).then(r=>r.json());
    statusEl.textContent = 'Rescan done. Added: ' + (out.added ?? '?');
  }catch(e){
    statusEl.textContent = 'Error: ' + e.message;
  }
});

load();
