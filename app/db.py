from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional
from pathlib import Path

from .settings import settings

engine = create_engine(f"sqlite:///{settings.DB_PATH}", echo=False)

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path: str
    type: str  # video|audio|image
    size: int
    duration: Optional[float] = 0.0
    width: Optional[int] = 0
    height: Optional[int] = 0
    vcodec: Optional[str] = None
    acodec: Optional[str] = None
    folder: Optional[str] = None

def init_db():
    settings.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
