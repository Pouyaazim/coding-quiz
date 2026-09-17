from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import User, Question, Attempt
from dependencies import require_admin, require_writer

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates")


# ----------------------------
# ریدایرکت ریشه ادمین
# ----------------------------
@router.get("/")
def admin_root(user: User = Depends(require_admin)):
    return RedirectResponse(url="/admin/dashboard", status_code=303)


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
# لیست کاربران + جستجو
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


# ----------------------------
# تغییر نقش کاربر
# ----------------------------
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


# ----------------------------
# حذف کاربر
# ----------------------------
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

    # اول تلاش‌ها رو حذف کن (چون FK دارن)
    db.query(Attempt).filter(Attempt.user_id == user_id).delete()
    db.delete(target)
    db.commit()

    return RedirectResponse(url="/admin/users", status_code=303)