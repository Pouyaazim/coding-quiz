from database import SessionLocal
from models import Question

db = SessionLocal()

questions = [
    {
        "text": "خروجی print(type(5)) چی هست؟",
        "option_a": "<class 'int'>",
        "option_b": "<class 'str'>",
        "option_c": "<class 'float'>",
        "option_d": "خطا می‌ده",
        "correct_option": "a",
        "category": "python",
        "difficulty": "easy",
        "xp_reward": 10,
    },
    {
        "text": "برای تعریف یه تابع تو پایتون از چه کلمه‌ای استفاده می‌کنیم؟",
        "option_a": "function",
        "option_b": "def",
        "option_c": "fun",
        "option_d": "define",
        "correct_option": "b",
        "category": "python",
        "difficulty": "easy",
        "xp_reward": 10,
    },
    {
        "text": "کدوم یکی از اینا لیست تو پایتونه؟",
        "option_a": "(1, 2, 3)",
        "option_b": "{1, 2, 3}",
        "option_c": "[1, 2, 3]",
        "option_d": "<1, 2, 3>",
        "correct_option": "c",
        "category": "python",
        "difficulty": "easy",
        "xp_reward": 10,
    },
    {
        "text": "تو جاوااسکریپت، برای تعریف متغیر غیرقابل‌تغییر از چی استفاده می‌کنیم؟",
        "option_a": "var",
        "option_b": "let",
        "option_c": "const",
        "option_d": "def",
        "correct_option": "c",
        "category": "javascript",
        "difficulty": "easy",
        "xp_reward": 10,
    },
    {
        "text": "خروجی 2 ** 3 تو پایتون چیه؟",
        "option_a": "6",
        "option_b": "8",
        "option_c": "9",
        "option_d": "23",
        "correct_option": "b",
        "category": "python",
        "difficulty": "easy",
        "xp_reward": 10,
    },
]

for q in questions:
    db.add(Question(**q))

db.commit()
db.close()
print(f"✅ {len(questions)} Questions added")