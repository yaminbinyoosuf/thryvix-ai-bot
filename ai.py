import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def build_system_prompt(bot_number: str, bot_code: str) -> str:
    return (
        "You are Thryvix AI, a smart, professional lead assistant.\n"
        "Always reply concisely and try to qualify leads and book a demo.\n"
        f"If this is the FIRST reply, include:\n📞 WhatsApp: {bot_number}\n🔑 Code: {bot_code}\n"
    )

def chat_completion(messages):
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content
