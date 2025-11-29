import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router

# Configure Structured Logging (JSON format for production)
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer()
    ]
)

app = FastAPI(title="Wall Robot Planner")

# Allow Frontend to talk to Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "wall-robot-planner"}

