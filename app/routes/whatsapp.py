"""
WhatsApp Routes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is the single endpoint Twilio calls into when a WhatsApp
message arrives:

1) /whatsapp/webhook -> triggered every time a customer sends a message

Unlike phone calls, WhatsApp has no "incoming call" step — every
message is just a fresh webhook call. We use the sender's phone
number (From) as the session key to remember the conversation.
"""

from fastapi import APIRouter, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from app.services.sales_agent import SalesAgent

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

# Temporary in-memory storage for active conversations
# (in real production this should be replaced with Redis or a database)
active_sessions: dict[str, SalesAgent] = {}


@router.post("/webhook")
async def whatsapp_webhook(From: str = Form(...), Body: str = Form("")):
    """
    Triggered every time a customer sends a WhatsApp message.
    Twilio sends the sender's number (From) and the message text (Body).
    """
    agent = active_sessions.get(From)
    if agent is None:
        agent = SalesAgent()
        active_sessions[From] = agent

    reply_text = agent.get_response(Body)

    response = MessagingResponse()
    response.message(reply_text)

    return Response(content=str(response), media_type="application/xml")
