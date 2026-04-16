from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.skills import Skill
from app.models.courses import Course
from app.schemas.skill import SkillCreate, SkillResponse
from app.routes.auth import require_role
from app.models.user import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=SkillResponse)
def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    # Check course exists
    course = db.query(Course).filter(Course.id == skill.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    new_skill = Skill(
        name=skill.name,
        course_id=skill.course_id
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


@router.get("/course/{course_id}", response_model=list[SkillResponse])
def list_skills(course_id: int, db: Session = Depends(get_db)):
    return db.query(Skill).filter(Skill.course_id == course_id).all()