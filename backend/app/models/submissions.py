from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("users.id"))
    assessment_id = Column(Integer, ForeignKey("assessments.id"))

    score = Column(Integer, nullable=False)

    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("User")
    assessment = relationship("Assessment")