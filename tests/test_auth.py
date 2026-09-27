from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models import User


def register(client, username, email=None, password="password123"):
    if email is None:
        email = f"{username}@test.com"
    return client.post(
        "/register",
        data={"username": username, "email": email, "password": password},
        follow_redirects=False,
    )


def login(client, username, password="password123"):
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )


def test_register_success():
    with TestClient(app) as client:
        response = register(client, "ali")
        assert response.status_code == 303

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "ali").first()
        assert user is not None
        assert user.email == "ali@test.com"
        assert user.hashed_password != "password123"
    finally:
        db.close()


def test_first_user_becomes_admin():
    with TestClient(app) as client:
        register(client, "first")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "first").first()
        assert user.role == "admin"
    finally:
        db.close()


def test_second_user_is_standard():
    with TestClient(app) as client:
        register(client, "first")
    with TestClient(app) as client:
        register(client, "second")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "second").first()
        assert user.role == "standard"
    finally:
        db.close()


def test_register_duplicate_username():
    with TestClient(app) as client:
        register(client, "ali", "ali@test.com")
    with TestClient(app) as client:
        response = register(client, "ali", "other@test.com")
        assert response.status_code == 200
        assert "قبلاً استفاده شده" in response.text


def test_register_duplicate_email():
    with TestClient(app) as client:
        register(client, "ali", "ali@test.com")
    with TestClient(app) as client:
        response = register(client, "other", "ali@test.com")
        assert response.status_code == 200
        assert "قبلاً استفاده شده" in response.text


def test_login_success():
    with TestClient(app) as client:
        register(client, "ali")
    with TestClient(app) as client:
        response = login(client, "ali")
        assert response.status_code == 303
        home = client.get("/")
        assert "ali" in home.text


def test_login_wrong_password():
    with TestClient(app) as client:
        register(client, "ali")
    with TestClient(app) as client:
        response = login(client, "ali", password="wrongpass")
        assert response.status_code == 200
        assert "اشتباه" in response.text


def test_login_nonexistent_user():
    with TestClient(app) as client:
        response = login(client, "ghost")
        assert response.status_code == 200
        assert "اشتباه" in response.text


def test_logout():
    with TestClient(app) as client:
        register(client, "ali")
    with TestClient(app) as client:
        login(client, "ali")
        response = client.get("/logout", follow_redirects=False)
        assert response.status_code == 303
        home = client.get("/")
        assert "خوش اومدی،" not in home.text