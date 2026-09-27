from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models import User, Question, Attempt
from auth import hash_password


def create_user(username, role="standard", password="password123"):
    db = SessionLocal()
    try:
        user = User(
            username=username,
            email=f"{username}@test.com",
            hashed_password=hash_password(password),
            role=role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user.id
    finally:
        db.close()


def login(client, username, password="password123"):
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )


def test_quiz_requires_login():
    with TestClient(app) as client:
        response = client.get("/quiz", follow_redirects=False)
        assert response.status_code == 303
        assert "/login" in response.headers["location"]


def test_quiz_returns_question():
    create_user("user")
    with TestClient(app) as client:
        login(client, "user")
        response = client.get("/quiz")
        assert response.status_code == 200
        assert "ثبت جواب" in response.text


def test_submit_correct_answer_adds_xp():
    user_id = create_user("user")
    db = SessionLocal()
    try:
        question = db.query(Question).first()
        question_id = question.id
        correct_option = question.correct_option
        xp_reward = question.xp_reward
    finally:
        db.close()

    with TestClient(app) as client:
        login(client, "user")
        response = client.post(
            f"/quiz/{question_id}",
            data={"selected_option": correct_option},
        )
        assert response.status_code == 200
        assert "درست بود" in response.text
        assert f"+{xp_reward} XP" in response.text

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        assert user.xp == xp_reward
    finally:
        db.close()


def test_submit_wrong_answer_no_xp():
    user_id = create_user("user")
    db = SessionLocal()
    try:
        question = db.query(Question).first()
        question_id = question.id
        correct_option = question.correct_option
        wrong_option = "a" if correct_option != "a" else "b"
    finally:
        db.close()

    with TestClient(app) as client:
        login(client, "user")
        response = client.post(
            f"/quiz/{question_id}",
            data={"selected_option": wrong_option},
        )
        assert response.status_code == 200
        assert "اشتباه بود" in response.text

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        assert user.xp == 0
    finally:
        db.close()


def test_submit_creates_attempt():
    user_id = create_user("user")
    db = SessionLocal()
    try:
        question = db.query(Question).first()
        question_id = question.id
        correct_option = question.correct_option
    finally:
        db.close()

    with TestClient(app) as client:
        login(client, "user")
        client.post(
            f"/quiz/{question_id}",
            data={"selected_option": correct_option},
        )

    db = SessionLocal()
    try:
        count = db.query(Attempt).filter(Attempt.user_id == user_id).count()
        assert count == 1
    finally:
        db.close()