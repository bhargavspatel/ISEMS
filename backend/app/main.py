from fastapi import FastAPI
from app.database import engine, Base
from app.models import user  
from app.routes.auth import router as auth_router
import app.models.courses
from app.routes.courses import router as courses_router
from app.routes.skills import router as skills_router
import app.models.assessments
import app.models.submissions
import app.models.skills
from app.routes.assessments import router as assessments_router
from app.routes.submissions import router as submissions_router
import app.models.mastery
from app.routes.mastery import router as mastery_router
import app.models.recommendations
from app.routes.recommendations import router as recommendations_router
from app.routes.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI()
origins = [
    "http://localhost:5173",   # React frontend
    "http://127.0.0.1:5173"
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

api.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api.include_router(courses_router, prefix="/courses", tags=["Courses"])
api.include_router(skills_router, prefix="/skills", tags=["Skills"])
api.include_router(assessments_router, prefix="/assessments", tags=["Assessments"])
api.include_router(submissions_router, prefix="/submissions", tags=["Submissions"])
api.include_router(mastery_router, prefix="/mastery", tags=["Mastery"])
api.include_router(recommendations_router, prefix="/recommendations", tags=["Recommendations"])
api.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])

@api.get("/")
def root():
    return {"message": "ISEMS Backend Running"}