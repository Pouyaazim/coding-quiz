import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Request, Depends, HTTPException, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from models import User, Question, Attempt
from leveling import level_progress
from auth import hash_password, verify_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")

AVATAR_DIR = Path("static/avatars")
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB


@router.get("/profile")
def profile(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    total_attempts = db.query(Attempt).filter(Attempt.user_id == user.id).count()
    correct_attempts = db.query(Attempt).filter(
        Attempt.user_id == user.id,
        Attempt.is_correct == True,
    ).count()
    wrong_attempts = total_attempts - correct_attempts
    accuracy = round((correct_attempts / total_attempts) * 100, 1) if total_attempts > 0 else 0

    higher_count = db.query(User).filter(User.xp > user.xp).count()
    rank = higher_count + 1
    total_users = db.query(User).count()

    progress = level_progress(user.xp)

    recent_attempts = (
        db.query(Attempt)
        .filter(Attempt.user_id == user.id)
        .order_by(Attempt.created_at.desc())
        .limit(10)
        .all()
    )

    best_category = (
        db.query(
            Question.category,
            func.count(Attempt.id).label("count"),
        )
        .join(Attempt)
        .filter(Attempt.user_id == user.id, Attempt.is_correct == True)
        .group_by(Question.category)
        .order_by(func.count(Attempt.id).desc())
        .first()
    )

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "user": user,
            "progress": progress,
            "total_attempts": total_attempts,
            "correct_attempts": correct_attempts,
            "wrong_attempts": wrong_attempts,
            "accuracy": accuracy,
            "rank": rank,
            "total_users": total_users,
            "recent_attempts": recent_attempts,
            "best_category": best_category.category if best_category else None,
        },
    )


@router.get("/profile/edit")
def profile_edit_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="profile_edit.html",
        context={"user": user, "error": None, "success": None},
    )


@router.post("/profile/edit")
def profile_edit(
    request: Request,
    email: str = Form(...),
    current_password: str = Form(""),
    new_password: str = Form(""),
    avatar: UploadFile = File(None),
    remove_avatar: str = Form(""),
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    def render_error(msg):
        return templates.TemplateResponse(
            request=request,
            name="profile_edit.html",
            context={"user": user, "error": msg, "success": None},
        )

    # چک ایمیل تکراری
    if email != user.email:
        existing = db.query(User).filter(User.email == email, User.id != user.id).first()
        if existing:
            return render_error("این ایمیل قبلاً استفاده شده")

    # چک رمز
    if new_password:
        if len(new_password) < 6:
            return render_error("رمز جدید باید حداقل ۶ کاراکتر باشه")
        if not current_password or not verify_password(current_password, user.hashed_password):
            return render_error("رمز فعلی اشتباهه")
        user.hashed_password = hash_password(new_password)

    # حذف عکس پروفایل
    if remove_avatar == "yes" and user.avatar:
        old_path = AVATAR_DIR / user.avatar
        if old_path.exists():
            old_path.unlink()
        user.avatar = None

    # آپلود عکس جدید
    if avatar and avatar.filename:
        ext = Path(avatar.filename).suffix.lower()

        if ext not in ALLOWED_EXTENSIONS:
            return render_error("فرمت عکس مجاز نیست. فقط jpg، png، gif، webp")

        # چک حجم
        content = avatar.file.read()
        if len(content) > MAX_FILE_SIZE:
            return render_error("حجم عکس نباید بیشتر از ۲ مگابایت باشه")

        # پاک کردن عکس قبلی
        if user.avatar:
            old_path = AVATAR_DIR / user.avatar
            if old_path.exists():
                old_path.unlink()

        # ذخیره فایل جدید
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = AVATAR_DIR / filename
        with open(filepath, "wb") as f:
            f.write(content)

        user.avatar = filename

    user.email = email
    db.commit()
    db.refresh(user)

    return templates.TemplateResponse(
        request=request,
        name="profile_edit.html",
        context={
            "user": user,
            "error": None,
            "success": "پروفایل با موفقیت ذخیره شد ✅",
        },
    )