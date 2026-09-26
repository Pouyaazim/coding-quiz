from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import text, inspect
from sqlalchemy.orm import Session

from database import get_db, Base, engine, SessionLocal
from models import User, Question
from leveling import level_progress
from routers import auth_routes, quiz_routes, admin_routes, profile_routes


def run_migrations():
    """اضافه کردن ستون‌های جدید به جداول موجود"""
    try:
        inspector = inspect(engine)
        if "users" not in inspector.get_table_names():
            return

        existing_columns = {col["name"] for col in inspector.get_columns("users")}

        migrations = [
            ("avatar_data", "ALTER TABLE users ADD COLUMN avatar_data TEXT"),
        ]

        with engine.connect() as conn:
            for column_name, sql in migrations:
                if column_name not in existing_columns:
                    try:
                        conn.execute(text(sql))
                        conn.commit()
                        print(f"Migration: added column '{column_name}' to users")
                    except Exception as e:
                        print(f"Migration failed for '{column_name}': {e}")
                        conn.rollback()
    except Exception as e:
        print(f"Warning: Migration check failed: {e}")


def init_database():
    """ساخت جدول‌ها و اضافه کردن سوالات پیش‌فرض اگه دیتابیس خالیه"""
    from add_questions import questions as seed_questions

    try:
        Path("static/avatars").mkdir(parents=True, exist_ok=True)
        Base.metadata.create_all(bind=engine)
        print("Tables created/verified.")
        run_migrations()

        try:
            db = SessionLocal()
            try:
                count = db.query(Question).count()
                if count == 0:
                    print("No questions found, seeding initial questions...")
                    for q in seed_questions:
                        db.add(Question(**q))
                    db.commit()
                    print(f"Seeded {len(seed_questions)} questions.")
                else:
                    print(f"Database already has {count} questions.")
            finally:
                db.close()
        except Exception as e:
            print(f"Warning: Could not seed questions: {e}")
    except Exception as e:
        print(f"Warning: init_database failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    init_database()
    print("Startup complete!")
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

Path("static").mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(SessionMiddleware, secret_key="my-super-secret-key-change-me-12345")

templates = Jinja2Templates(directory="templates")

app.include_router(auth_routes.router)
app.include_router(quiz_routes.router)
app.include_router(admin_routes.router)
app.include_router(profile_routes.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    user = None
    progress = None
    if user_id:
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                progress = level_progress(user.xp)
        except Exception as e:
            print(f"Error loading user: {e}")
            user = None

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"user": user, "progress": progress},
    )