from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.routes.auth import require_role
from app.models.user import User
from app.models.courses import Course
from app.models.skills import Skill
from app.models.mastery import Mastery
from app.models.recommendations import Recommendation
import json

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    courses = db.query(Course).all()

    dashboard_data = {
        "student_name": current_user.name,
        "courses": []
    }

    for course in courses:
        skills = db.query(Skill).filter(Skill.course_id == course.id).all()

        skill_list = []

        for skill in skills:
            mastery = db.query(Mastery).filter(
                Mastery.student_id == current_user.id,
                Mastery.skill_id == skill.id
            ).first()

            recommendation = db.query(Recommendation).filter(
                Recommendation.student_id == current_user.id,
                Recommendation.skill_id == skill.id
            ).first()

            skill_list.append({
                "skill_id": skill.id,
                "skill_name": skill.name,
                "mastery_score": mastery.mastery_score if mastery else 0,
                "recommendation": json.loads(recommendation.recommendation_text) if recommendation else None
            })

        dashboard_data["courses"].append({
            "course_id": course.id,
            "course_title": course.title,
            "skills": skill_list
        })

    return dashboard_data