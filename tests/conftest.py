import os
import tempfile
from pathlib import Path

TEST_DB_PATH = Path(tempfile.gettempdir()) / "coding_quiz_test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"

import pytest

from database import SessionLocal, Base, engine
from models import User, Attempt, Question


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink()
        except PermissionError:
            pass

    Base.metadata.create_all(bind=engine)

    # seed سوالات
    from add_questions import questions as seed_questions
    db = SessionLocal()
    try:
        for q in seed_questions:
            db.add(Question(**q))
        db.commit()
    finally:
        db.close()

    yield

    engine.dispose()
    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink()
        except PermissionError:
            pass


@pytest.fixture(autouse=True)
def clean_state():
    db = SessionLocal()
    try:
        db.query(Attempt).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()
    yield