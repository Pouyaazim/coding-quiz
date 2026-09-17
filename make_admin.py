from database import SessionLocal
from models import User

db = SessionLocal()
username = input("username that you want as admin=>  ")

user = db.query(User).filter(User.username == username).first()
if not user:
    print("❌ user not found")
else:
    user.role = "admin"
    db.commit()
    print(f"✅ {username} admin now")

db.close()