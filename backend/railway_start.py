"""Safety-first cloud launcher. Never reset an existing family's database."""
import os
import secrets
import sqlite3
from pathlib import Path

def start():
    os.environ["PKM_DB_ENGINE"] = "sqlite"
    os.environ["PKM_CLOUD_MODE"] = "1"
    if not os.getenv("PKM_SQLITE_FILE", "").startswith("/data/"):
        raise SystemExit("Set PKM_SQLITE_FILE=/data/pkm.sqlite3 and mount a persistent Railway volume at /data.")
    from app.config import DATA_DIR
    from app.db import DBFILE
    secret = os.getenv("PKM_JWT_SECRET", "")
    if len(secret) < 32 or secret == "dev-only-secret-change-me":
        raise SystemExit("Set a unique PKM_JWT_SECRET (at least 32 characters).")
    if os.getenv("PKM_PARENT_PASSWORD", "") in ("", "admin123") or len(os.getenv("PKM_PARENT_PASSWORD", "")) < 12:
        raise SystemExit("Set PKM_PARENT_PASSWORD to a unique password of at least 12 characters.")
    if not os.getenv("PKM_PARENT_ID") or not os.getenv("PKM_CHILD_PIN") or os.getenv("PKM_CHILD_PIN") in ("1234","0000","1111"):
        raise SystemExit("Set PKM_PARENT_ID and a unique PKM_CHILD_PIN before deploying.")
    if not Path(DATA_DIR, "00_schema.sql").is_file():
        raise SystemExit("Missing generated assets/out/00_schema.sql; follow ASSETS_GUIDE.md before deployment.")
    dbfile = Path(DBFILE)
    dbfile.parent.mkdir(parents=True, exist_ok=True)
    if dbfile.exists():
        with sqlite3.connect(dbfile) as conn:
            row = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='parent_user'").fetchone()
        if not row:
            raise SystemExit("Existing DB lacks parent_user: refusing destructive initialization. Restore or inspect backup.")
        print("Existing family DB detected: preserving all progress.", flush=True)
    else:
        from app.init_db import main
        print("New DB: one-time initialization.", flush=True)
        main()
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), proxy_headers=True)

if __name__ == "__main__":
    start()
