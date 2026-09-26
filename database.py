import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# 1. خوندن آدرس دیتابیس از متغیر محیطی (برای Pxxl/Neon)
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. اگه متغیر نبود، از SQLite لوکال استفاده کن
if not DATABASE_URL:
    BASE_DIR = Path(__file__).resolve().parent
    DATABASE_URL = f"sqlite:///{BASE_DIR / 'quiz.db'}"

# 3. اصلاح URL برای SQLAlchemy 2.0
# بعضی سرویس‌ها با postgres:// می‌دن، SQLAlchemy 2.0 می‌خواد postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 4. ساخت engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
    )

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()