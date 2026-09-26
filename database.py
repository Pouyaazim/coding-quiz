import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# مسیر پوشه‌ای که این فایل توشه
BASE_DIR = Path(__file__).resolve().parent

# اگه رو Pxxl هستیم و پوشه read-only بود، از /tmp استفاده کن
try:
    test_file = BASE_DIR / ".write_test"
    test_file.touch()
    test_file.unlink()
    DB_PATH = BASE_DIR / "quiz.db"
except (OSError, PermissionError):
    DB_PATH = Path("/tmp") / "quiz.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"

print(f"Database path: {DB_PATH}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()