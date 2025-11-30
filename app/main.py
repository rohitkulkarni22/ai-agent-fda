from fastapi import FastAPI
from app.api.endpoints import router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(router, prefix="/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the FDA Food Adverse Event AI Agent API"}
