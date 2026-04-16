from pydantic import BaseModel


class CourseCreate(BaseModel):
    title: str


class CourseResponse(BaseModel):
    id: int
    title: str
    instructor_id: int

    class Config:
        from_attributes = True