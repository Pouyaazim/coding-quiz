from database import SessionLocal
from models import User

db = SessionLocal()
username = input("اسم کاربری که میخوای ادمین کنی: ")

user = db.query(User).filter(User.username == username).first()
if not user:
    print("❌ کاربر پیدا نشد")
else:
    user.role = "admin"
    db.commit()
    print(f"✅ {username} حالا ادمینه")

db.close()