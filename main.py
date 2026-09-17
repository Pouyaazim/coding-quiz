from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from models import User, Question, Attempt
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

# ----------------------------
# کوییز
# ----------------------------
import random


@app.get("/quiz")
def quiz(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    # یه سوال تصادفی که کاربر قبلاً جوابش نداده
    answered_ids = [
        a.question_id for a in
        db.query(Attempt).filter(Attempt.user_id == user_id).all()
    ]

    query = db.query(Question)
    if answered_ids:
        query = query.filter(~Question.id.in_(answered_ids))

    questions = query.all()

    if not questions:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "is_correct": True,
                "xp_reward": 0,
                "new_xp": 0,
                "new_level": 0,
                "correct_answer": "همه سوالا رو جواب دادی! 🎉",
                "no_question": True,
            }
        )

    question = random.choice(questions)

    return templates.TemplateResponse(
        request=request,
        name="quiz.html",
        context={"question": question}
    )


@app.post("/quiz/{question_id}")
def submit_answer(
    question_id: int,
    request: Request,
    selected_option: str = Form(...),
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(User).filter(User.id == user_id).first()
    question = db.query(Question).filter(Question.id == question_id).first()

    if not user or not question:
        raise HTTPException(status_code=404, detail="چیزی پیدا نشد")

    is_correct = selected_option == question.correct_option

    # ثبت تلاش
    attempt = Attempt(
        user_id=user.id,
        question_id=question.id,
        selected_option=selected_option,
        is_correct=is_correct,
    )
    db.add(attempt)

    # اگه درست بود، XP بده
    xp_reward = 0
    if is_correct:
        xp_reward = question.xp_reward
        user.xp += xp_reward
        # محاسبه سطح جدید: هر ۱۰۰ XP یه سطح
        user.level = user.xp // 100

    db.commit()
    db.refresh(user)

    correct_answer_text = getattr(question, f"option_{question.correct_option}")

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "is_correct": is_correct,
            "xp_reward": xp_reward,
            "new_xp": user.xp,
            "new_level": user.level,
            "correct_answer": correct_answer_text,
        }
    )