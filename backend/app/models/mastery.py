from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Mastery(Base):
    __tablename__ = "mastery"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("users.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))

    mastery_score = Column(Float, nullable=False)

    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("User")
    skill = relationship("Skill")