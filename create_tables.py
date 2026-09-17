from database import Base, engine
import models  # این import لازمه تا جدول‌ها شناخته بشن

Base.metadata.create_all(bind=engine)
print("✅ جداول ساخته شدند")