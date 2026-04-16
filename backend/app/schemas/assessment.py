from pydantic import BaseModel


class AssessmentCreate(BaseModel):
    title: str
    max_score: int
    skill_id: int


class AssessmentResponse(BaseModel):
    id: int
    title: str
    max_score: int
    skill_id: int

    class Config:
        from_attributes = True