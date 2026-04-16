from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    assessment_id: int
    score: int


class SubmissionResponse(BaseModel):
    id: int
    student_id: int
    assessment_id: int
    score: int

    class Config:
        from_attributes = True