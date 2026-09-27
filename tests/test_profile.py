from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models import User
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


def test_profile_requires_login():
    with TestClient(app) as client:
        response = client.get("/profile", follow_redirects=False)
        assert response.status_code == 303


def test_profile_shows_user_info():
    create_user("user")
    with TestClient(app) as client:
        login(client, "user")
        response = client.get("/profile")
        assert response.status_code == 200
        assert "user@test.com" in response.text


def test_public_profile_accessible():
    create_user("admin", role="admin")
    create_user("user")

    # admin از client جدا لاگین میکنه
    with TestClient(app) as admin_client:
        login(admin_client, "admin")
        response = admin_client.get("/u/user")
        assert response.status_code == 200
        assert "user" in response.text


def test_public_profile_nonexistent():
    create_user("user")
    with TestClient(app) as client:
        login(client, "user")
        response = client.get("/u/ghost")
        assert response.status_code == 404


def test_public_profile_own_redirects_to_profile():
    create_user("user")
    with TestClient(app) as client:
        login(client, "user")
        response = client.get("/u/user", follow_redirects=False)
        assert response.status_code == 303
        assert "/profile" in response.headers["location"]


def test_edit_profile_email():
    user_id = create_user("user")
    with TestClient(app) as client:
        login(client, "user")
        response = client.post(
            "/profile/edit",
            data={"email": "newemail@test.com", "current_password": "", "new_password": ""},
        )
        assert response.status_code == 200

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        assert user.email == "newemail@test.com"
    finally:
        db.close()


def test_edit_profile_password_change():
    create_user("user")
    with TestClient(app) as client:
        login(client, "user")
        response = client.post(
            "/profile/edit",
            data={"email": "user@test.com", "current_password": "password123", "new_password": "newpassword456"},
        )
        assert response.status_code == 200

    # لاگین با رمز جدید
    with TestClient(app) as client:
        response = login(client, "user", password="newpassword456")
        assert response.status_code == 303


def test_edit_profile_wrong_current_password():
    create_user("user")
    with TestClient(app) as client:
        login(client, "user")
        response = client.post(
            "/profile/edit",
            data={"email": "user@test.com", "current_password": "wrongpass", "new_password": "newpassword456"},
        )
        assert response.status_code == 200
        assert "رمز فعلی اشتباهه" in response.text