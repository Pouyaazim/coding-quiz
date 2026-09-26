import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. خواندن آدرس دیتابیس از متغیرهای محیطی (برای Pxxl)
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. اگر متغیر محیطی وجود نداشت، از SQLite برای اجرای لوکال استفاده کن
if not DATABASE_URL:
    BASE_DIR = Path(__file__).resolve().parent
    DATABASE_URL = f"sqlite:///{BASE_DIR / 'quiz.db'}"

# 3. ساخت موتور دیتابیس
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # برای PostgreSQL، به آرگومان‌های اضافی نیازی نیست
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()