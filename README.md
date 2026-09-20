<div align="center">

# 🎮 Coding Quiz

**یه پلتفرم بازی-آموزش برنامه‌نویسی با گیمیفیکیشن، رقابت و پنل مدیریت**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

---

## 📖 درباره پروژه

یادگیری برنامه‌نویسی حوصله‌سربره. خیلی‌ها دوره‌های آموزشی رو تموم می‌کنن ولی چون تمرین کافی ندارن، خیلی زود مطالب رو فراموش می‌کنن.

**Coding Quiz** این مشکل رو با گیمیفیکیشن حل می‌کنه:

- 🎯 کاربرا به سوالات برنامه‌نویسی جواب میدن
- ⚡ با هر پاسخ درست، XP می‌گیرن و Level آپ میکنن
- 🏆 تو Leaderboard با بقیه رقابت می‌کنن
- 👤 پروفایل شخصی و عمومی دارن
- 🛠 مدیران میتونن سوالات و کاربرا رو مدیریت کنن

---

## 🖼 اسکرین‌شات‌ها

### صفحه اصلی
![Home](screenshots/01-home.png)

### کوییز
![Quiz](screenshots/02-quiz.png)

### نتیجه کوییز
![Result](screenshots/03-result.png)

### لیست بهترین‌ها
![Leaderboard](screenshots/04-leaderboard.png)

### پروفایل کاربر
![Profile](screenshots/05-profile.png)

### داشبورد ادمین
![Admin Dashboard](screenshots/06-admin-dashboard.png)

### تحلیل تلاش‌ها
![Admin Attempts](screenshots/07-admin-attempts.png)

---

## ✨ امکانات

### 👤 کاربر عادی
- ثبت‌نام، ورود، خروج (با session امن)
- کوییز با سوالات تصادفی از بین ۱۰۰+ سوال
- سیستم XP و Level با فرمول پیشرفته (`50 × level²`)
- Progress bar برای پیشرفت به لول بعدی
- Leaderboard با ۲۰ نفر برتر
- پروفایل شخصی با آواتار
- ویرایش پروفایل (ایمیل، رمز، عکس)
- مشاهده پروفایل عمومی بقیه کاربرا

### ✍️ Writer
- همه امکانات کاربر عادی
- ورود به پنل مدیریت
- افزودن سوال جدید
- ویرایش سوالات موجود

### 🛠 Admin
- همه امکانات Writer
- داشبورد آماری (تعداد کاربر، سوال، تلاش، دقت)
- مدیریت کاربران (تغییر نقش، حذف، جستجو)
- مشاهده پروفایل کامل هر کاربر
- لاگ تلاش‌ها با نمودارهای تعاملی
- فیلتر دوره زمانی (۷، ۱۴، ۳۰، ۹۰ روز)
- حذف سوالات

---

## 🏗 معماری پروژه

```
coding-quize/
├── main.py                    # نقطه شروع اپلیکیشن
├── database.py                # اتصال به دیتابیس
├── models.py                  # مدل‌های SQLAlchemy
├── auth.py                    # هش کردن رمز
├── leveling.py                # فرمول محاسبه لول
├── dependencies.py            # وابستگی‌های نقش‌محور
├── create_tables.py           # ساخت جداول
├── add_questions.py           # اضافه کردن سوالات نمونه
├── make_admin.py              # تبدیل کاربر به ادمین
├── routers/                   # روترهای FastAPI
│   ├── auth_routes.py         # ثبت‌نام، ورود، خروج
│   ├── quiz_routes.py         # کوییز، نتیجه، leaderboard
│   ├── profile_routes.py      # پروفایل شخصی و عمومی
│   └── admin_routes.py        # پنل مدیریت
├── templates/                 # قالب‌های Jinja2
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── quiz.html
│   ├── result.html
│   ├── leaderboard.html
│   ├── profile.html
│   ├── profile_edit.html
│   ├── public_profile.html
│   └── admin/
│       ├── base.html
│       ├── dashboard.html
│       ├── users.html
│       ├── user_detail.html
│       ├── questions.html
│       ├── question_form.html
│       └── attempts.html
├── static/
│   └── avatars/               # عکس‌های پروفایل کاربران
└── screenshots/               # عکس‌های README
```

---

## 🚀 تکنولوژی‌ها

### Backend
- **FastAPI** — فریم‌ورک وب مدرن و سریع
- **SQLAlchemy 2.0** — ORM برای کار با دیتابیس
- **SQLite** — دیتابیس سبک (قابل ارتقا به PostgreSQL)
- **Pydantic** — اعتبارسنجی داده
- **Passlib** — هش کردن رمز عبور
- **Starlette SessionMiddleware** — مدیریت session

### Frontend
- **Jinja2** — موتور قالب
- **Chart.js** — نمودارهای تعاملی
- **HTML/CSS** — طراحی سفارشی با تم تیره

### DevTools
- **Git** — کنترل نسخه
- **Python venv** — محیط مجازی

---

## 🔐 سیستم نقش‌ها (RBAC)

| نقش | دسترسی |
|---|---|
| `standard` | استفاده از کوییز، پروفایل شخصی، leaderboard |
| `writer` | + افزودن و ویرایش سوالات |
| `admin` | + مدیریت کاربران، داشبورد، حذف سوالات |

نقش‌ها با `Depends` تو FastAPI محافظت میشن:
```python
@router.get("/admin/dashboard")
def dashboard(user: User = Depends(require_admin)):
    ...
```

---

## 📊 فرمول لولینگ

لول کاربر از XP با فرمول زیر حساب میشه:

```
XP needed for level N = 50 × N²
```

| لول | XP کل لازم | XP لازم تو این لول |
|-----|-----------|-------------------|
| ۰ → ۱ | ۵۰ | ۵۰ |
| ۱ → ۲ | ۲۰۰ | ۱۵۰ |
| ۲ → ۳ | ۴۵۰ | ۲۵۰ |
| ۳ → ۴ | ۸۰۰ | ۳۵۰ |
| ۴ → ۵ | ۱۲۵۰ | ۴۵۰ |

**حس پیشرفت:** هر لول سخت‌تر از قبلی، مثل بازی‌های واقعی.

---

## 🛠 نصب و اجرا

### پیش‌نیازها
- Python 3.12+
- Git

### مراحل

**۱. کلون پروژه:**
```bash
git clone https://github.com/Pouyaazim/coding-quiz.git
cd coding-quiz
```

**۲. ساخت محیط مجازی:**
```bash
python -m venv .venv
```

**۳. فعال‌سازی محیط مجازی:**

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

**۴. نصب کتابخانه‌ها:**
```bash
pip install -r requirements.txt
```

**۵. ساخت دیتابیس:**
```bash
python create_tables.py
python add_questions.py
```

**۶. اجرای سرور:**
```bash
uvicorn main:app --reload
```

**۷. باز کن تو مرورگر:**
```
http://127.0.0.1:8000
```

---

## 🔑 ساخت ادمین

بعد از ثبت‌نام با یه کاربر:

```bash
python make_admin.py
```

اسم کاربری که میخوای ادمین بشه رو وارد کن.

---

## 📡 API Endpoints

مستندات خودکار FastAPI در دسترسه:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### نمونه endpointها

| Method | Path | توضیح |
|---|---|---|
| GET | `/` | صفحه اصلی |
| POST | `/register` | ثبت‌نام |
| POST | `/login` | ورود |
| GET | `/logout` | خروج |
| GET | `/quiz` | شروع کوییز |
| POST | `/quiz/{id}` | ارسال پاسخ |
| GET | `/leaderboard` | لیست بهترین‌ها |
| GET | `/profile` | پروفایل شخصی |
| GET | `/u/{username}` | پروفایل عمومی |
| GET | `/admin/dashboard` | داشبورد ادمین |
| GET | `/admin/users` | مدیریت کاربران |
| GET | `/admin/questions` | مدیریت سوالات |
| GET | `/admin/attempts` | تحلیل تلاش‌ها |

---

## 🗺 نقشه راه

- [x] سیستم احراز هویت با session
- [x] کوییز با XP و Level
- [x] سیستم نقش‌ها (standard/writer/admin)
- [x] Leaderboard
- [x] پروفایل کاربر با آواتار
- [x] پروفایل عمومی
- [x] پنل مدیریت کامل
- [x] نمودارهای آماری
- [ ] تست با pytest
- [ ] دیپلوی روی سرور
- [ ] Docker
- [ ] WebSocket برای مسابقه real-time
- [ ] Badge و Achievement

---

## 🤝 مشارکت

اگه ایده یا پیشنهادی داری:

1. Fork کن
2. Branch بساز (`git checkout -b feature/amazing-feature`)
3. کامیت کن (`git commit -m 'Add amazing feature'`)
4. Push کن (`git push origin feature/amazing-feature`)
5. Pull Request بزن

---

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده. فایل `LICENSE` رو ببین.

---

## 👨‍💻 سازنده

**پویا عظیم**

- GitHub: [@Pouyaazim](https://github.com/Pouyaazim)

---

<div align="center">

**⭐ اگه این پروژه بهت کمک کرد، یه ستاره بده! ⭐**

</div>