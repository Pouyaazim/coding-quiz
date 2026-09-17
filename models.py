from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    attempts = relationship("Attempt", back_populates="user")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)          # متن سوال
    option_a = Column(String, nullable=False)      # گزینه ۱
    option_b = Column(String, nullable=False)      # گزینه ۲
    option_c = Column(String, nullable=False)      # گزینه ۳
    option_d = Column(String, nullable=False)      # گزینه ۴
    correct_option = Column(String, nullable=False)  # "a" یا "b" یا "c" یا "d"
    category = Column(String, default="python")    # دسته‌بندی: python, js, ...
    difficulty = Column(String, default="easy")    # سطح: easy, medium, hard
    xp_reward = Column(Integer, default=10)        # امتیاز این سوال


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_option = Column(String, nullable=False)  # گزینه‌ای که کاربر انتخاب کرد
    is_correct = Column(Boolean, default=False)       # درست بود یا نه
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="attempts")