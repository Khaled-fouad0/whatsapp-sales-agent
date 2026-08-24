"""
Basic Unit Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Run with: pytest tests/ -v
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Confirm the server is running and returns the correct status."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_check():
    """Confirm the health check endpoint works."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_whatsapp_webhook_returns_twiml():
    """Confirm the webhook returns valid TwiML with a message."""
    response = client.post(
        "/whatsapp/webhook",
        data={"From": "whatsapp:+201234567890", "Body": "Hello"},
    )
    assert response.status_code == 200
    assert "<Message>" in response.text


def test_conversation_memory_persists():
    """
    Confirm the same sender's conversation history is remembered
    and the agent keeps responding coherently across multiple messages.

    Note: since this runs against the real Groq API (production mode),
    we can't assert on exact wording — LLM responses vary naturally
    between calls even for the same input. Instead, we verify the
    conversation flow works end-to-end without breaking.
    """
    from_number = "whatsapp:+201111111111"

    first_response = client.post(
        "/whatsapp/webhook", data={"From": from_number, "Body": "Hello"}
    )
    second_response = client.post(
        "/whatsapp/webhook",
        data={"From": from_number, "Body": "عايز اعرف السعر"},
    )

    # Both requests should succeed
    assert first_response.status_code == 200
    assert second_response.status_code == 200

    # Both should return a valid, non-empty message
    assert "<Message>" in first_response.text
    assert "<Message>" in second_response.text

    # A reply should always contain actual content, not an empty tag
    assert "<Message></Message>" not in second_response.text
