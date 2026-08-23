"""
Main Entry Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is where everything comes together and the server starts.
"""

from fastapi import FastAPI
from app.routes import whatsapp
from app.config import settings

app = FastAPI(
    title="WhatsApp Sales Agent",
    description="AI-powered WhatsApp sales agent built with Twilio + Groq",
    version="1.0.0",
)

app.include_router(whatsapp.router)


@app.get("/")
async def root():
    """Simple health-check endpoint to confirm the server is running."""
    return {
        "status": "running",
        "service": "WhatsApp Sales Agent",
        "mode": "mock" if settings.is_mock_mode else "production",
    }


@app.get("/health")
async def health_check():
    """Used by Docker/hosting platforms to verify the server is alive."""
    return {"status": "healthy"}
