from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]
DB_FILE = Path(os.getenv("DB_FILE", str(BASE_DIR / "data" / "db.json")))

DB_BACKEND = os.getenv("DB_BACKEND", "sqlite").lower()

if DB_BACKEND == "sqlite":
    sqlite_path = Path(os.getenv("SQLITE_PATH", str(BASE_DIR / "data" / "app.db")))
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    DB_URL = f"sqlite:///{sqlite_path}"
elif DB_BACKEND == "postgres":
    DB_URL = os.getenv("DATABASE_URL", "")
else:
    DB_URL = ""
