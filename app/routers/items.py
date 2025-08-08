from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from sqlmodel import select, func
from pathlib import Path

from ..db import Item, get_session

router = APIRouter(prefix="/api", tags=["items"])

@router.get("/items")
def list_items(
    type: Optional[str] = Query(default=None),
    q: Optional[str] = Query(default=None),
    limit: int = 100,
    offset: int = 0,
):
    with get_session() as s:
        stmt = select(Item)
        if type in {"video", "audio", "image"}:
            stmt = stmt.where(Item.type == type)

        if q:
            # naive filter in Python for SQLite (no ILIKE)
            rows = [r for r in s.exec(stmt).all() if q.lower() in Path(r.path).name.lower()]
            total = len(rows)
            return {"items": rows[offset:offset + limit], "total": total}

        # correct way to count rows
        total = s.exec(select(func.count()).select_from(Item)).one()
        rows = s.exec(stmt.offset(offset).limit(limit)).all()
        return {"items": rows, "total": total}

@router.get("/items/{item_id}")
def get_item(item_id: int):
    with get_session() as s:
        item = s.get(Item, item_id)
        if not item:
            raise HTTPException(404, "Not found")
        return item
