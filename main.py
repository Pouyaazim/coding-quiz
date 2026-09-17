from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from database import get_db
from auth import hash_password, verify_password
from models import User

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="my-super-secret-key-change-me-12345")

templates = Jinja2Templates(directory="templates")


# ----------------------------
# صفحه اصلی
# ----------------------------
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    user = None
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"user": user}
    )


# ----------------------------
# ثبت‌نام
# ----------------------------
@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@app.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "این نام کاربری یا ایمیل قبلاً استفاده شده"}
        )

    new_user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/", status_code=303)


# ----------------------------
# ورود
# ----------------------------
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@app.post("/login")
def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "نام کاربری یا رمز اشتباهه"}
        )

    request.session["user_id"] = user.id

    return RedirectResponse(url="/", status_code=303)


# ----------------------------
# خروج ← این آخرین بخشه
# ----------------------------
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)