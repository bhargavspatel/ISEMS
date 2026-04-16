from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.assessments import Assessment
from app.models.skills import Skill
from app.schemas.assessment import AssessmentCreate, AssessmentResponse
from app.routes.auth import require_role
from app.models.user import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=AssessmentResponse)
def create_assessment(
    assessment: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    skill = db.query(Skill).filter(Skill.id == assessment.skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    new_assessment = Assessment(
        title=assessment.title,
        max_score=assessment.max_score,
        skill_id=assessment.skill_id
    )

    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    return new_assessment


@router.get("/skill/{skill_id}", response_model=list[AssessmentResponse])
def list_assessments(skill_id: int, db: Session = Depends(get_db)):
    return db.query(Assessment).filter(Assessment.skill_id == skill_id).all()