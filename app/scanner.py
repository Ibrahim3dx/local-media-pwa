from pathlib import Path
from typing import Iterable, List, Tuple
import os, subprocess, json

from .db import Item, get_session
from .settings import settings

VIDEO_EXT = {".mp4", ".mkv", ".webm", ".avi"}
AUDIO_EXT = {".mp3", ".aac", ".flac", ".wav"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

def media_type_for(path: Path) -> str | None:
    ext = path.suffix.lower()
    if ext in VIDEO_EXT: return "video"
    if ext in AUDIO_EXT: return "audio"
    if ext in IMAGE_EXT: return "image"
    return None

def ffprobe(path: Path) -> dict:
    try:
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name,width,height", "-of", "json", str(path)]
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        data = json.loads(out)
    except Exception:
        return {}
    res = {"duration": 0.0, "width": 0, "height": 0, "vcodec": None, "acodec": None}
    if "format" in data and "duration" in data["format"]:
        try: res["duration"] = float(data["format"]["duration"])
        except: pass
    streams = data.get("streams", [])
    for s in streams:
        if s.get("width"):
            res["width"] = max(res["width"] or 0, s.get("width", 0))
            res["height"] = max(res["height"] or 0, s.get("height", 0))
            res["vcodec"] = s.get("codec_name", res["vcodec"])
        elif s.get("codec_name"):
            res["acodec"] = s.get("codec_name", res["acodec"])
    return res

def scan_once(root: Path) -> int:
    count = 0
    root = root.resolve()
    with get_session() as s:
        for dirpath, _, filenames in os.walk(root):
            for name in filenames:
                p = Path(dirpath) / name
                mtype = media_type_for(p)
                if not mtype: continue
                stat = p.stat()
                meta = ffprobe(p) if mtype != "image" else {}
                item = Item(
                    path=str(p),
                    type=mtype,
                    size=stat.st_size,
                    duration=meta.get("duration", 0.0),
                    width=meta.get("width", 0),
                    height=meta.get("height", 0),
                    vcodec=meta.get("vcodec"),
                    acodec=meta.get("acodec"),
                    folder=str(Path(dirpath).relative_to(root))
                )
                s.add(item)
                count += 1
        s.commit()
    return count
