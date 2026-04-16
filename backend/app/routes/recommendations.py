from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.recommendations import Recommendation
from app.routes.auth import require_role
from app.models.user import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{skill_id}")
def get_recommendation(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    rec = db.query(Recommendation).filter(
        Recommendation.student_id == current_user.id,
        Recommendation.skill_id == skill_id
    ).first()

    if not rec:
        raise HTTPException(status_code=404, detail="No recommendation found")

    return {
        "skill_id": skill_id,
        "recommendation": rec.recommendation_text
    }