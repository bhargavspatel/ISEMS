from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    max_score = Column(Integer, nullable=False)

    skill_id = Column(Integer, ForeignKey("skills.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    skill = relationship("Skill")