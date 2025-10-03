import os
import openai

# Set API key globally
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def build_system_prompt(bot_number: str, bot_code: str) -> str:
    return (
        "You are Thryvix AI, a smart, professional lead assistant.\n"
        "1) Be concise, friendly, and professional.\n"
        "2) Ask questions to qualify leads and book a demo.\n"
        "3) Mirror user's language (Malayalam/Hindi script or Manglish/Hinglish).\n"
        "4) If this is the FIRST reply, include this header once:\n"
        f"📞 WhatsApp: {bot_number}\n🔑 Code: {bot_code}\n"
        "5) Keep answers under 4 short lines.\n"
    )

def chat_completion(messages):
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message["content"]
