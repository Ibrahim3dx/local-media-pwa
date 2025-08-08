from fastapi import APIRouter, HTTPException, Response, Request
from pathlib import Path
from ..db import Item, get_session

router = APIRouter(prefix="/api", tags=["stream"])

def partial_content(file_path: Path, range_header: str | None):
    file_size = file_path.stat().st_size
    start, end = 0, file_size - 1
    if range_header and range_header.startswith("bytes="):
        rng = range_header.split("=")[1]
        s, e = rng.split("-")[0], rng.split("-")[1] if "-" in rng else ""
        if s: start = int(s)
        if e: end = int(e) if e else end
    start = max(0, start); end = min(end, file_size - 1)
    length = end - start + 1
    with open(file_path, "rb") as f:
        f.seek(start)
        data = f.read(length)
    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(length),
    }
    return data, headers, 206 if range_header else 200

@router.get("/stream/{item_id}")
def stream_file(item_id: int, request: Request):
    with get_session() as s:
        item = s.get(Item, item_id)
        if not item: raise HTTPException(404, "Not found")
        p = Path(item.path)
        if not p.exists(): raise HTTPException(404, "File missing")
        data, headers, status = partial_content(p, request.headers.get("range"))
        # naive content type
        if item.type == "video":
            ct = "video/mp4"
        elif item.type == "audio":
            ct = "audio/mpeg"
        else:
            ct = "image/jpeg"
        return Response(content=data, status_code=status, headers=headers, media_type=ct)
