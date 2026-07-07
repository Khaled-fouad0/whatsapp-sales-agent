"""
Sales Agent Service (WhatsApp)
================================
This is the "brain" of the agent. It takes the customer's
WhatsApp message and returns a smart sales reply.

Two modes:
1) Mock Mode: simple keyword-based replies - for testing without API keys.
   Keyword detection matches Arabic phrases (since real customers write
   in Arabic), but replies are hardcoded in English for now.
2) Real Mode: uses Groq (Llama 3) to generate dynamic, intelligent replies.
   The agent automatically replies in the same language the customer
   used (Arabic or English), based on explicit instructions in the
   system prompt.
"""

from app.config import settings

SYSTEM_PROMPT = """
You are a professional, friendly sales representative for a software company,
chatting with a customer over WhatsApp.
Your job:
1. Greet the customer warmly
2. Understand their need
3. Offer the right solution briefly
4. Try to book a follow-up call or close the sale
Keep your answers short and clear, like a real WhatsApp conversation
(2-4 sentences max, no long paragraphs).

IMPORTANT: Always reply in the same language the customer used in their
last message. If they wrote in Arabic, reply fully in Arabic (Egyptian
dialect). If they wrote in English, reply fully in English.
Never mix two languages in the same reply.
"""


class SalesAgent:
    def __init__(self):
        self.conversation_history: list[dict] = []
        self.mock_mode = settings.is_mock_mode

    def _mock_reply(self, user_text: str) -> str:
        """Simple rule-based reply for testing without real API keys."""
        text = user_text.lower()

        price_keywords = ["سعر", "تكلفة", "price", "cost"]
        greeting_keywords = ["مرحبا", "السلام", "hello", "hi"]
        booking_keywords = ["موعد", "احجز", "appointment", "book"]
        rejection_keywords = ["لا", "مش عايز", "no", "not interested"]

        if any(word in text for word in price_keywords):
            return "Our basic plan starts at $99/month and includes all the tools you need. Want me to book a call with our sales team?"
        elif any(word in text for word in greeting_keywords):
            return "Hi there! 👋 This is the AI sales assistant. How can I help you today?"
        elif any(word in text for word in booking_keywords):
            return "Sure! What day and time works best for you?"
        elif any(word in text for word in rejection_keywords):
            return "No problem at all, thanks for your time! Feel free to reach out anytime. 🙌"
        else:
            return "Got it! We provide AI automation solutions that save your company time and money. Want to hear more details?"

    def get_response(self, user_text: str) -> str:
        """Main entry point: takes customer message, returns agent reply."""
        self.conversation_history.append({"role": "user", "content": user_text})

        if self.mock_mode:
            reply = self._mock_reply(user_text)
        else:
            reply = self._real_groq_reply(user_text)

        self.conversation_history.append({"role": "assistant", "content": reply})
        return reply

    def _real_groq_reply(self, user_text: str) -> str:
        """
        Real mode: calls Groq's API (auto-activates once GROQ_API_KEY
        is set in .env). Groq uses the same request format as OpenAI,
        so we reuse the 'openai' Python library, just pointing it to
        Groq's endpoint instead.
        """
        from openai import OpenAI

        client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.conversation_history

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=150,
        )
        return response.choices[0].message.content