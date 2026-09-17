from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models import User


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User | None:
    """کاربر لاگین‌شده رو برمی‌گردونه، یا None"""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


def require_login(user: User = Depends(get_current_user)) -> User:
    """اگه کاربر لاگین نباشه، 403 می‌ده"""
    if not user:
        raise HTTPException(status_code=403, detail="اول باید وارد بشی")
    return user


def require_writer(user: User = Depends(require_login)) -> User:
    """فقط writer یا admin"""
    if user.role not in ("writer", "admin"):
        raise HTTPException(status_code=403, detail="دسترسی نداری")
    return user


def require_admin(user: User = Depends(require_login)) -> User:
    """فقط admin"""
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="فقط ادمین")
    return user