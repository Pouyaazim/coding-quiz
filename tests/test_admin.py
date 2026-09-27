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


def test_admin_dashboard_requires_admin():
    create_user("user", role="standard")
    with TestClient(app) as client:
        login(client, "user")
        response = client.get("/admin/dashboard")
        assert response.status_code == 403


def test_admin_dashboard_accessible_by_admin():
    create_user("admin", role="admin")
    with TestClient(app) as client:
        login(client, "admin")
        response = client.get("/admin/dashboard")
        assert response.status_code == 200
        assert "داشبورد" in response.text


def test_admin_users_list():
    create_user("admin", role="admin")
    with TestClient(app) as client:
        login(client, "admin")
        response = client.get("/admin/users")
        assert response.status_code == 200


def test_standard_cannot_access_users():
    create_user("user", role="standard")
    with TestClient(app) as client:
        login(client, "user")
        response = client.get("/admin/users")
        assert response.status_code == 403


def test_admin_can_change_user_role():
    create_user("admin", role="admin")
    user_id = create_user("user", role="standard")

    with TestClient(app) as client:
        login(client, "admin")
        response = client.post(
            f"/admin/users/{user_id}/role",
            data={"role": "writer"},
            follow_redirects=False,
        )
        assert response.status_code == 303

    db = SessionLocal()
    try:
        target = db.query(User).filter(User.id == user_id).first()
        assert target.role == "writer"
    finally:
        db.close()


def test_admin_cannot_change_own_role():
    admin_id = create_user("admin", role="admin")

    with TestClient(app) as client:
        login(client, "admin")
        response = client.post(
            f"/admin/users/{admin_id}/role",
            data={"role": "standard"},
        )
        assert response.status_code == 400


def test_admin_can_delete_user():
    create_user("admin", role="admin")
    user_id = create_user("user", role="standard")

    with TestClient(app) as client:
        login(client, "admin")
        response = client.post(
            f"/admin/users/{user_id}/delete",
            follow_redirects=False,
        )
        assert response.status_code == 303

    db = SessionLocal()
    try:
        target = db.query(User).filter(User.id == user_id).first()
        assert target is None
    finally:
        db.close()


def test_admin_cannot_delete_self():
    admin_id = create_user("admin", role="admin")

    with TestClient(app) as client:
        login(client, "admin")
        response = client.post(f"/admin/users/{admin_id}/delete")
        assert response.status_code == 400


def test_writer_can_access_questions():
    create_user("writer", role="writer")
    with TestClient(app) as client:
        login(client, "writer")
        response = client.get("/admin/questions")
        assert response.status_code == 200


def test_standard_cannot_access_questions():
    create_user("user", role="standard")
    with TestClient(app) as client:
        login(client, "user")
        response = client.get("/admin/questions")
        assert response.status_code == 403


def test_writer_cannot_access_users():
    create_user("writer", role="writer")
    with TestClient(app) as client:
        login(client, "writer")
        response = client.get("/admin/users")
        assert response.status_code == 403


def test_admin_attempts_page():
    create_user("admin", role="admin")
    with TestClient(app) as client:
        login(client, "admin")
        response = client.get("/admin/attempts")
        assert response.status_code == 200