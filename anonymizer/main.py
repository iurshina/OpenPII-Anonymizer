from fastapi import FastAPI
from anonymizer.db.database import init_db
from anonymizer.api.routes import router as api_router
from anonymizer.utils.logger import setup_logger

logger = setup_logger("anonymizer")

logger.info("Starting application...")

app = FastAPI(
    title="PII Anonymization API",
    description="An API for detecting, resolving, and anonymizing PII in text using LLMs.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    """
    Actions to perform when the application starts.
    """
    init_db() 

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the PII Anonymization API"}