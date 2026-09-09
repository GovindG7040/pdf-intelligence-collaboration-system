from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.documents import router as documents_router
from app.core.config import settings

app = FastAPI(
    title="PDF Intelligence & Collaboration System",
    description="AI-powered PDF intelligence and collaboration platform.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(documents_router)

@app.get("/")
def root():
    return {
        "message": "PDF Intelligence & Collaboration System API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }