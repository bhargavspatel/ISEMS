from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.submissions import Submission
from app.models.assessments import Assessment
from app.models.mastery import Mastery
from app.models.recommendations import Recommendation
from app.models.skills import Skill
from app.schemas.submission import SubmissionCreate, SubmissionResponse
from app.routes.auth import require_role
from app.models.user import User
from app.services.mastery_engine import calculate_mastery
from app.services.ai_engine import generate_ai_feedback
import json

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=SubmissionResponse)
def submit_assessment(
    submission: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    # 1️⃣ Validate assessment
    assessment = db.query(Assessment).filter(
        Assessment.id == submission.assessment_id
    ).first()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    if submission.score > assessment.max_score:
        raise HTTPException(status_code=400, detail="Score exceeds max score")

    # 2️⃣ Save submission
    new_submission = Submission(
        student_id=current_user.id,
        assessment_id=submission.assessment_id,
        score=submission.score
    )

    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    # 3️⃣ Calculate mastery
    skill_id = assessment.skill_id

    recent_submissions = (
        db.query(Submission)
        .join(Submission.assessment)
        .filter(
            Submission.student_id == current_user.id,
            Assessment.skill_id == skill_id
        )
        .order_by(Submission.submitted_at.desc())
        .all()
    )

    mastery_score = calculate_mastery(recent_submissions)

    existing_mastery = db.query(Mastery).filter(
        Mastery.student_id == current_user.id,
        Mastery.skill_id == skill_id
    ).first()

    if existing_mastery:
        existing_mastery.mastery_score = mastery_score
    else:
        new_mastery = Mastery(
            student_id=current_user.id,
            skill_id=skill_id,
            mastery_score=mastery_score
        )
        db.add(new_mastery)

    db.commit()

    # 4️⃣ Generate AI Recommendation
    skill = db.query(Skill).filter(Skill.id == skill_id).first()

    if mastery_score < 0.75:
        recent_scores = [s.score for s in recent_submissions[:3]]

        ai_output = generate_ai_feedback(
            skill.name,
            mastery_score,
            recent_scores
        )

        recommendation_text = json.dumps(ai_output)
    else:
        recommendation_text = json.dumps({
            "summary": "Strong performance.",
            "weakness_analysis": "No significant weaknesses detected.",
            "recommended_actions": ["Attempt advanced challenges."],
            "confidence_level": "high"
        })

    # 5️⃣ Store Recommendation
    existing_rec = db.query(Recommendation).filter(
        Recommendation.student_id == current_user.id,
        Recommendation.skill_id == skill_id
    ).first()

    if existing_rec:
        existing_rec.recommendation_text = recommendation_text
    else:
        new_rec = Recommendation(
            student_id=current_user.id,
            skill_id=skill_id,
            recommendation_text=recommendation_text
        )
        db.add(new_rec)

    db.commit()

    return new_submission