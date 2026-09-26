from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from database import get_db, Base, engine, SessionLocal
from models import User, Question
from leveling import level_progress
from routers import auth_routes, quiz_routes, admin_routes, profile_routes


def init_database():
    """ساخت جدول‌ها و اضافه کردن سوالات پیش‌فرض اگه دیتابیس خالیه"""
    from add_questions import questions as seed_questions

    Path("static/avatars").mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)

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


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    user = None
    progress = None
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            progress = level_progress(user.xp)

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"user": user, "progress": progress},
    )