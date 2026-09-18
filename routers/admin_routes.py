from datetime import datetime, timedelta
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, Integer
from sqlalchemy.orm import Session

from database import get_db
from models import User, Question, Attempt
from dependencies import require_admin, require_writer

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates")


# ----------------------------
# ورودی هوشمند پنل
# ----------------------------
@router.get("/panel")
def admin_panel_entry(user: User = Depends(require_writer)):
    """ادمین → داشبورد، writer → سوالات"""
    if user.role == "admin":
        return RedirectResponse(url="/admin/dashboard", status_code=303)
    return RedirectResponse(url="/admin/questions", status_code=303)


# ----------------------------
# داشبورد
# ----------------------------
@router.get("/dashboard")
def dashboard(
    request: Request,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    total_users = db.query(User).count()
    total_questions = db.query(Question).count()
    total_attempts = db.query(Attempt).count()
    correct_attempts = db.query(Attempt).filter(Attempt.is_correct == True).count()

    accuracy = 0
    if total_attempts > 0:
        accuracy = round((correct_attempts / total_attempts) * 100, 1)

    recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "current_user": user,
            "total_users": total_users,
            "total_questions": total_questions,
            "total_attempts": total_attempts,
            "accuracy": accuracy,
            "recent_users": recent_users,
        },
    )


# ----------------------------
# لیست کاربران
# ----------------------------
@router.get("/users")
def users_list(
    request: Request,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
    q: str = "",
):
    query = db.query(User)
    if q:
        query = query.filter(
            (User.username.contains(q)) | (User.email.contains(q))
        )
    users = query.order_by(User.created_at.desc()).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/users.html",
        context={
            "current_user": user,
            "users": users,
            "q": q,
        },
    )


@router.post("/users/{user_id}/role")
def change_role(
    user_id: int,
    role: str = Form(...),
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    if target.id == user.id:
        raise HTTPException(status_code=400, detail="نمیتونی نقش خودت رو عوض کنی")

    if role not in ("standard", "writer", "admin"):
        raise HTTPException(status_code=400, detail="نقش نامعتبر")

    target.role = role
    db.commit()

    return RedirectResponse(url="/admin/users", status_code=303)


@router.post("/users/{user_id}/delete")
def delete_user(
    user_id: int,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="کاربر پیدا نشد")

    if target.id == user.id:
        raise HTTPException(status_code=400, detail="نمیتونی خودت رو حذف کنی")

    db.query(Attempt).filter(Attempt.user_id == user_id).delete()
    db.delete(target)
    db.commit()

    return RedirectResponse(url="/admin/users", status_code=303)


# ----------------------------
# مدیریت سوالات
# ----------------------------
@router.get("/questions")
def questions_list(
    request: Request,
    user: User = Depends(require_writer),
    db: Session = Depends(get_db),
):
    questions = db.query(Question).order_by(Question.id.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/questions.html",
        context={
            "current_user": user,
            "questions": questions,
        },
    )


@router.get("/questions/new")
def question_new_page(
    request: Request,
    user: User = Depends(require_writer),
):
    return templates.TemplateResponse(
        request=request,
        name="admin/question_form.html",
        context={
            "current_user": user,
            "question": None,
        },
    )


@router.post("/questions/new")
def question_create(
    request: Request,
    text: str = Form(...),
    option_a: str = Form(...),
    option_b: str = Form(...),
    option_c: str = Form(...),
    option_d: str = Form(...),
    correct_option: str = Form(...),
    category: str = Form("python"),
    difficulty: str = Form("easy"),
    xp_reward: int = Form(10),
    user: User = Depends(require_writer),
    db: Session = Depends(get_db),
):
    if correct_option not in ("a", "b", "c", "d"):
        raise HTTPException(status_code=400, detail="گزینه درست باید a، b، c یا d باشه")

    q = Question(
        text=text,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_option=correct_option,
        category=category,
        difficulty=difficulty,
        xp_reward=xp_reward,
    )
    db.add(q)
    db.commit()

    return RedirectResponse(url="/admin/questions", status_code=303)


@router.get("/questions/{question_id}/edit")
def question_edit_page(
    question_id: int,
    request: Request,
    user: User = Depends(require_writer),
    db: Session = Depends(get_db),
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="سوال پیدا نشد")

    return templates.TemplateResponse(
        request=request,
        name="admin/question_form.html",
        context={
            "current_user": user,
            "question": question,
        },
    )


@router.post("/questions/{question_id}/edit")
def question_update(
    question_id: int,
    request: Request,
    text: str = Form(...),
    option_a: str = Form(...),
    option_b: str = Form(...),
    option_c: str = Form(...),
    option_d: str = Form(...),
    correct_option: str = Form(...),
    category: str = Form("python"),
    difficulty: str = Form("easy"),
    xp_reward: int = Form(10),
    user: User = Depends(require_writer),
    db: Session = Depends(get_db),
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="سوال پیدا نشد")

    if correct_option not in ("a", "b", "c", "d"):
        raise HTTPException(status_code=400, detail="گزینه درست باید a، b، c یا d باشه")

    question.text = text
    question.option_a = option_a
    question.option_b = option_b
    question.option_c = option_c
    question.option_d = option_d
    question.correct_option = correct_option
    question.category = category
    question.difficulty = difficulty
    question.xp_reward = xp_reward

    db.commit()

    return RedirectResponse(url="/admin/questions", status_code=303)


@router.post("/questions/{question_id}/delete")
def question_delete(
    question_id: int,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="سوال پیدا نشد")

    db.query(Attempt).filter(Attempt.question_id == question_id).delete()
    db.delete(question)
    db.commit()

    return RedirectResponse(url="/admin/questions", status_code=303)


# ----------------------------
# لاگ تلاش‌ها
# ----------------------------
@router.get("/attempts")
def attempts_list(
    request: Request,
    user: User = Depends(require_admin),
    db: Session = Depends(get_db),
    filter_type: str = "all",
    period: int = 7,
):
    if period not in (7, 14, 30, 90):
        period = 7

    query = db.query(Attempt).join(User).join(Question)

    if filter_type == "correct":
        query = query.filter(Attempt.is_correct == True)
    elif filter_type == "wrong":
        query = query.filter(Attempt.is_correct == False)

    attempts = query.order_by(Attempt.created_at.desc()).limit(100).all()

    total = db.query(Attempt).count()
    correct_count = db.query(Attempt).filter(Attempt.is_correct == True).count()
    wrong_count = total - correct_count
    accuracy = round((correct_count / total) * 100, 1) if total > 0 else 0

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_count = db.query(Attempt).filter(Attempt.created_at >= today_start).count()

    period_start = datetime.utcnow() - timedelta(days=period)
    daily_stats = (
        db.query(
            func.date(Attempt.created_at).label("day"),
            func.count(Attempt.id).label("total"),
            func.sum(func.cast(Attempt.is_correct, Integer)).label("correct"),
        )
        .filter(Attempt.created_at >= period_start)
        .group_by(func.date(Attempt.created_at))
        .order_by(func.date(Attempt.created_at))
        .all()
    )

    days = []
    daily_total = []
    daily_correct = []

    for i in range(period):
        day = (datetime.utcnow() - timedelta(days=period - 1 - i)).date()
        days.append(day.strftime("%m/%d"))

        found = None
        for stat in daily_stats:
            if str(stat.day) == str(day):
                found = stat
                break

        if found:
            daily_total.append(found.total)
            daily_correct.append(found.correct or 0)
        else:
            daily_total.append(0)
            daily_correct.append(0)

    difficulty_stats = (
        db.query(
            Question.difficulty,
            func.count(Attempt.id).label("count"),
        )
        .join(Attempt)
        .group_by(Question.difficulty)
        .all()
    )
    difficulty_labels = [d.difficulty for d in difficulty_stats]
    difficulty_data = [d.count for d in difficulty_stats]

    category_stats = (
        db.query(
            Question.category,
            func.count(Attempt.id).label("count"),
        )
        .join(Attempt)
        .group_by(Question.category)
        .all()
    )
    category_labels = [c.category for c in category_stats]
    category_data = [c.count for c in category_stats]

    active_users_today = (
        db.query(func.count(func.distinct(Attempt.user_id)))
        .filter(Attempt.created_at >= today_start)
        .scalar()
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/attempts.html",
        context={
            "current_user": user,
            "attempts": attempts,
            "filter_type": filter_type,
            "period": period,
            "total": total,
            "correct_count": correct_count,
            "wrong_count": wrong_count,
            "accuracy": accuracy,
            "today_count": today_count,
            "active_users_today": active_users_today,
            "days": days,
            "daily_total": daily_total,
            "daily_correct": daily_correct,
            "difficulty_labels": difficulty_labels,
            "difficulty_data": difficulty_data,
            "category_labels": category_labels,
            "category_data": category_data,
        },
    )