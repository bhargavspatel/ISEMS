from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.mastery import Mastery
from app.routes.auth import require_role
from app.models.user import User
from app.schemas.mastery import MasteryResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{skill_id}", response_model=MasteryResponse)
def get_mastery(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    mastery = db.query(Mastery).filter(
        Mastery.student_id == current_user.id,
        Mastery.skill_id == skill_id
    ).first()

    if not mastery:
        raise HTTPException(status_code=404, detail="No mastery record found")

    return mastery