from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.courses import Course
from app.schemas.course import CourseCreate, CourseResponse
from app.routes.auth import require_role
from app.models.user import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CourseResponse)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    new_course = Course(
        title=course.title,
        instructor_id=current_user.id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


@router.get("/", response_model=list[CourseResponse])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()