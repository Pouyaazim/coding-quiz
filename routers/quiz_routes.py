import random
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import User, Question, Attempt

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/quiz")
def quiz(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    answered_ids = [
        a.question_id for a in
        db.query(Attempt).filter(Attempt.user_id == user_id).all()
    ]

    query = db.query(Question)
    if answered_ids:
        query = query.filter(~Question.id.in_(answered_ids))

    questions = query.all()

    if not questions:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "is_correct": True,
                "xp_reward": 0,
                "new_xp": 0,
                "new_level": 0,
                "correct_answer": "همه سوالا رو جواب دادی! 🎉",
            },
        )

    question = random.choice(questions)
    return templates.TemplateResponse(
        request=request,
        name="quiz.html",
        context={"question": question},
    )


@router.post("/quiz/{question_id}")
def submit_answer(
    question_id: int,
    request: Request,
    selected_option: str = Form(...),
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(User).filter(User.id == user_id).first()
    question = db.query(Question).filter(Question.id == question_id).first()

    if not user or not question:
        raise HTTPException(status_code=404, detail="چیزی پیدا نشد")

    is_correct = selected_option == question.correct_option

    attempt = Attempt(
        user_id=user.id,
        question_id=question.id,
        selected_option=selected_option,
        is_correct=is_correct,
    )
    db.add(attempt)

    xp_reward = 0
    if is_correct:
        xp_reward = question.xp_reward
        user.xp += xp_reward
        user.level = user.xp // 100

    db.commit()
    db.refresh(user)

    correct_answer_text = getattr(question, f"option_{question.correct_option}")

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "is_correct": is_correct,
            "xp_reward": xp_reward,
            "new_xp": user.xp,
            "new_level": user.level,
            "correct_answer": correct_answer_text,
        },
    )