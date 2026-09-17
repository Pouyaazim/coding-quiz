from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import User, Question, Attempt
from dependencies import require_admin, require_writer

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates")


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


@router.get("/")
def admin_root(user: User = Depends(require_admin)):
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/admin/dashboard", status_code=303)