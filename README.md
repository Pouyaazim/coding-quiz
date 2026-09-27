<div align="center">

# 🎮 Coding Quiz

**یه پلتفرم بازی-آموزش برنامه‌نویسی با گیمیفیکیشن، رقابت و پنل مدیریت**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Tests](https://img.shields.io/badge/tests-34_passed-success?logo=pytest&logoColor=white)](#-تست‌ها)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

[🌐 دموی زنده](https://coding-quiz.pxxlspace.cv) · [📸 اسکرین‌شات‌ها](#-اسکرین‌شات‌ها) · [🐛 گزارش باگ](../../issues)

</div>

---

## 📖 درباره پروژه

یادگیری برنامه‌نویسی حوصله‌سربره. خیلی‌ها دوره‌های آموزشی رو تموم می‌کنن ولی چون تمرین کافی ندارن، خیلی زود مطالب رو فراموش می‌کنن.

**Coding Quiz** این مشکل رو با گیمیفیکیشن حل می‌کنه:

- 🎯 کاربرا به سوالات برنامه‌نویسی جواب میدن
- ⚡ با هر پاسخ درست، XP می‌گیرن و Level آپ می‌کنن
- 🏆 تو Leaderboard با بقیه رقابت می‌کنن
- 👤 پروفایل شخصی و عمومی دارن
- 🛠 مدیران میتونن سوالات و کاربرا رو مدیریت کنن

---

## ✨ امکانات

### 👤 کاربر عادی
- ثبت‌نام، ورود، خروج (session امن)
- کوییز با سوالات تصادفی از بین ۱۰۰+ سوال
- سیستم XP و Level با فرمول پیشرفته (`50 × level²`)
- Progress bar برای پیشرفت به لول بعدی
- Leaderboard با ۲۰ نفر برتر
- پروفایل شخصی با آواتار
- ویرایش پروفایل (ایمیل، رمز، عکس)
- مشاهده پروفایل عمومی بقیه کاربرا
- جستجوی کاربران

### ✍️ Writer
- همه امکانات کاربر عادی
- ورود به پنل مدیریت
- افزودن و ویرایش سوالات

### 🛠 Admin
- همه امکانات Writer
- داشبورد آماری (کاربر، سوال، تلاش، دقت)
- مدیریت کاربران (تغییر نقش، حذف، جستجو)
- مشاهده پروفایل کامل هر کاربر
- لاگ تلاش‌ها با نمودارهای تعاملی
- فیلتر دوره زمانی (۷، ۱۴، ۳۰، ۹۰ روز)
- حذف سوالات

---

## 🎨 طراحی و تجربه کاربری

- 🌌 **Aurora Background** — پس‌زمینه متحرک با ۴ blob رنگی
- 🪟 **Glassmorphism** — کارت‌های شفاف با blur حرفه‌ای
- 🎭 **3D Tilt** — کارت‌ها با ماوس می‌چرخن
- ✨ **Scroll Reveal** — المان‌ها با اسکرول ظاهر میشن
- 💫 **Animated Counters** — اعداد با انیمیشن شمارش میشن
- 🎯 **Shine Buttons** — دکمه‌ها با افکت براق
- 🎊 **Confetti** — جشن وقتی جواب درست میدی
- 📱 **کاملاً ریسپانسیو** — موبایل، تبلت، دسکتاپ
- 🎨 **فونت وزیرمتن** — خوانا و مدرن
- 🌙 **تم تیره** — راحت برای چشم

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

## 🏗 معماری پروژه

```
coding-quize/
├── main.py                    # نقطه شروع اپلیکیشن
├── database.py                # اتصال به دیتابیس (SQLite/PostgreSQL)
├── models.py                  # مدل‌های SQLAlchemy
├── auth.py                    # هش کردن رمز
├── leveling.py                # فرمول محاسبه لول
├── dependencies.py            # وابستگی‌های نقش‌محور
├── add_questions.py           # سوالات نمونه
├── make_admin.py              # تبدیل کاربر به ادمین
├── pytest.ini                 # تنظیمات تست
├── requirements.txt           # کتابخانه‌های production
├── requirements-dev.txt       # کتابخانه‌های development
├── routers/                   # روترهای FastAPI
│   ├── auth_routes.py         # ثبت‌نام، ورود، خروج
│   ├── quiz_routes.py         # کوییز، نتیجه، leaderboard
│   ├── profile_routes.py      # پروفایل شخصی و عمومی
│   └── admin_routes.py        # پنل مدیریت
├── templates/                 # قالب‌های Jinja2
│   ├── base.html              # قالب پایه با aurora
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
│       ├── base.html          # قالب پایه پنل ادمین
│       ├── dashboard.html
│       ├── users.html
│       ├── user_detail.html
│       ├── questions.html
│       ├── question_form.html
│       └── attempts.html
├── static/                    # فایل‌های استاتیک
│   ├── style.css              # استایل اصلی
│   ├── animations.css         # انیمیشن‌های حرفه‌ای
│   ├── animations.js          # اسکریپت‌های انیمیشن
│   ├── responsive.js          # مدیریت سایدبار موبایل
│   └── favicon.svg            # لوگو
├── tests/                     # تست‌های pytest
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_quiz.py
│   ├── test_profile.py
│   └── test_admin.py
└── screenshots/               # عکس‌های README
```

---

## 🚀 تکنولوژی‌ها

### Backend
- **FastAPI** — فریم‌ورک وب مدرن و سریع
- **SQLAlchemy 2.0** — ORM برای کار با دیتابیس
- **PostgreSQL / SQLite** — دیتابیس (بسته به محیط)
- **Pydantic** — اعتبارسنجی داده
- **Passlib** — هش کردن رمز عبور
- **Starlette SessionMiddleware** — مدیریت session

### Frontend
- **Jinja2** — موتور قالب
- **Chart.js** — نمودارهای تعاملی
- **Vanilla CSS** — طراحی سفارشی با glassmorphism
- **Vanilla JS** — انیمیشن‌ها بدون کتابخانه

### Testing & DevOps
- **pytest** — فریم‌ورک تست
- **httpx** — کلاینت HTTP برای تست
- **GitHub Actions** — CI/CD
- **Docker** — بسته‌بندی

---

## 🧪 تست‌ها

پروژه دارای **۳۴ تست** با pytest هست:

```bash
pytest
```

**پوشش تست:**

| فایل | تست‌ها |
|---|---|
| `test_auth.py` | ثبت‌نام، ورود، خروج، تکراری‌ها، ادمین اول |
| `test_quiz.py` | XP، تلاش، پاسخ درست/غلط |
| `test_profile.py` | مشاهده، ویرایش، پروفایل عمومی |
| `test_admin.py` | دسترسی admin/writer/standard، تغییر نقش، حذف |

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

**نکته:** اولین کاربری که ثبت‌نام کنه، **خودکار ادمین** میشه.

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

**۵. (اختیاری) نصب کتابخانه‌های توسعه:**
```bash
pip install -r requirements-dev.txt
```

**۶. اجرای سرور:**
```bash
uvicorn main:app --reload
```

**۷. باز کن تو مرورگر:**
```
http://127.0.0.1:8000
```

**نکته:** دیتابیس، جدول‌ها و سوالات **خودکار** موقع بالا اومدن سرور ساخته میشن.

---

## 🔑 ساخت ادمین

اولین کاربری که ثبت‌نام کنه، خودکار ادمین میشه. اگه میخوای کاربر دیگه‌ای رو ادمین کنی:

```bash
python make_admin.py
```

---

## 🌐 دیپلوی

پروژه روی **Pxxl** با **Neon PostgreSQL** دیپلوی شده.

### دیپلوی خودت

1. **دیتابیس PostgreSQL رایگان** از [Neon.tech](https://neon.tech) بگیر
2. **Connection String** رو به عنوان `DATABASE_URL` تو Environment Variables ست کن
3. کد رو push کن → دیپلوی خودکار

**Environment Variables مورد نیاز:**
```
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

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
| GET | `/profile/edit` | ویرایش پروفایل |
| GET | `/u/{username}` | پروفایل عمومی |
| GET | `/avatar/{user_id}` | عکس پروفایل |
| GET | `/admin/dashboard` | داشبورد ادمین |
| GET | `/admin/users` | مدیریت کاربران |
| GET | `/admin/questions` | مدیریت سوالات |
| GET | `/admin/attempts` | تحلیل تلاش‌ها |
| GET | `/health` | Health check |

---

## 🗺 نقشه راه

- [x] سیستم احراز هویت با session
- [x] کوییز با XP و Level پیشرفته
- [x] سیستم نقش‌ها (standard/writer/admin)
- [x] Leaderboard
- [x] پروفایل کاربر با آواتار (base64)
- [x] پروفایل عمومی
- [x] پنل مدیریت کامل
- [x] نمودارهای آماری تعاملی
- [x] UI/UX با انیمیشن‌های Awwwards
- [x] کاملاً ریسپانسیو
- [x] تست با pytest (۳۴ تست)
- [x] GitHub Actions CI
- [x] دیپلوی روی Pxxl + Neon
- [ ] Badge و Achievement
- [ ] WebSocket برای مسابقه real-time
- [ ] Docker

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