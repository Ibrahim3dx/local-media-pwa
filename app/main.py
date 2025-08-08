from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from pathlib import Path
import ipaddress

from .db import init_db
from .routers import items, stream, admin as admin_api

app = FastAPI(title="Local Media PWA")
init_db()

# API routers
app.include_router(items.router)
app.include_router(stream.router)
app.include_router(admin_api.router)

static_dir = Path(__file__).parent / "static"

# --- ADMIN PAGE (must be BEFORE the static mount) ---

def _is_localhost(request: Request):
    try:
        ip = ipaddress.ip_address(request.client.host if request.client else "")
        return ip.is_loopback
    except Exception:
        host_hdr = (request.headers.get("host") or "").split(":")[0].lower()
        return host_hdr in {"localhost", "127.0.0.1", "::1"}

@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request):
    if not _is_localhost(request):
        raise HTTPException(status_code=403, detail="Forbidden")
    return (static_dir / "admin.html").read_text(encoding="utf-8")

# --- STATIC served last ---
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
