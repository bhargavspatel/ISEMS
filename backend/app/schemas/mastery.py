from pydantic import BaseModel


class MasteryResponse(BaseModel):
    skill_id: int
    mastery_score: float

    class Config:
        from_attributes = True