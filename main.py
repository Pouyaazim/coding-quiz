from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import User
from leveling import level_progress
from routers import auth_routes, quiz_routes, admin_routes, profile_routes
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()
# پوشه static رو mount کن
Path("static/avatars").mkdir(parents=True, exist_ok=True)
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