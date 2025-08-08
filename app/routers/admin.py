from fastapi import APIRouter, Request, HTTPException
from ..settings import settings
from ..scanner import scan_once
from ..db import init_db
from pydantic import BaseModel

from pathlib import Path
import ipaddress

router = APIRouter(prefix="/api", tags=["admin"])

def _is_localhost(request: Request) -> bool:
    try:
        host = request.client.host if request.client else ""
        ip = ipaddress.ip_address(host)
        return ip.is_loopback  # True for 127.0.0.1 and ::1
    except Exception:
        # Fallback: accept common localhost hosts
        host_hdr = (request.headers.get("host") or "").split(":")[0].lower()
        return host_hdr in {"localhost", "127.0.0.1", "::1"}

class ConfigIn(BaseModel):
    media_root: str

@router.get("/health")
def health():
    return {"status": "ok", "root": str(settings.media_root())}

@router.get("/config")
def get_config(request: Request):
    if not _is_localhost(request):
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"media_root": str(settings.media_root())}

@router.put("/config")
def set_config(cfg: ConfigIn, request: Request):
    if not _is_localhost(request):
        raise HTTPException(status_code=403, detail="Forbidden")
    p = settings.set_media_root(cfg.media_root)
    return {"media_root": str(p)}

@router.post("/rescan")
def rescan(request: Request):
    if not _is_localhost(request):
        raise HTTPException(status_code=403, detail="Forbidden")
    init_db()
    count = scan_once(settings.media_root())
    return {"added": count}
