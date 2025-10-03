import os, openai

# Classic global client style to avoid proxy issues on Render
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = (
    "You are Thryvix AI, a smart, professional lead assistant for business automation.\n"
    "Goals:\n"
    "- Greet briefly and be human. Limit to 3–4 short lines.\n"
    "- Ask relevant questions to qualify the lead and move towards booking a demo.\n"
    "- Ask progressively: business type → city/location → WhatsApp or call demo preference.\n"
    "- Mirror the user's language: if they write Malayalam/Hindi in native script, reply in that script;\n"
    "  if they use Manglish/Hinglish (Romanized), reply in romanized form but clearer.\n"
    "- If user is confused, explain simply. If off-topic, gently steer back.\n"
    "- Never mention phone numbers or codes.\n"
)

def chat_completion(history):
    # history: list of dicts {role: system/user/assistant, content: str}
    resp = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=history,
        temperature=0.7,
    )
    return resp.choices[0].message["content"]
