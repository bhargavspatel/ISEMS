from pydantic import BaseModel


class SkillCreate(BaseModel):
    name: str
    course_id: int


class SkillResponse(BaseModel):
    id: int
    name: str
    course_id: int

    class Config:
        from_attributes = True