from pathlib import Path
import os
import json

class Settings:
    APP_DIR: Path = Path(__file__).resolve().parent
    CONFIG_PATH: Path = APP_DIR / "config.json"
    DB_PATH: Path = APP_DIR / "media.db"
    THUMBS_DIR: Path = APP_DIR / "thumbnails"
    HLS_ENABLED: bool = bool(os.environ.get("HLS_ENABLED", "0") == "1")

    def _load_config(self) -> dict:
        if self.CONFIG_PATH.exists():
            try:
                return json.loads(self.CONFIG_PATH.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def _save_config(self, cfg: dict) -> None:
        self.CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

    def media_root(self) -> Path:
        # Priority: saved config -> env var -> default Videos
        cfg = self._load_config()
        p = cfg.get("MEDIA_ROOT") or os.environ.get("MEDIA_ROOT")
        if p:
            return Path(p).expanduser().resolve()
        return Path.home() / "Videos"

    def set_media_root(self, path: str) -> Path:
        p = Path(path).expanduser().resolve()
        if not p.exists() or not p.is_dir():
            raise ValueError("Path does not exist or is not a directory")
        cfg = self._load_config()
        cfg["MEDIA_ROOT"] = str(p)
        self._save_config(cfg)
        return p

settings = Settings()
