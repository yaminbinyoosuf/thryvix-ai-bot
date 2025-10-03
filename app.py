import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from ai import build_system_prompt, chat_completion

app = Flask(__name__)

BOT_WHATSAPP_NUMBER = os.getenv("BOT_WHATSAPP_NUMBER", "+14155238886")
BOT_FIRST_CODE = os.getenv("BOT_FIRST_CODE", "THRYVIX2025")
MAX_HISTORY = int(os.getenv("MAX_HISTORY", "6"))  # messages (per role) to keep

# In-memory sessions: phone -> {'messages': [...], 'sent_header': bool}
SESSIONS = {}

def session_for(phone: str):
    if phone not in SESSIONS:
        SESSIONS[phone] = {"messages": [], "sent_header": False}
    return SESSIONS[phone]

def trim_history(msgs):
    # Keep last MAX_HISTORY*2 messages (user+assistant), excluding the system
    base = [m for m in msgs if m["role"] != "system"]
    if len(base) <= MAX_HISTORY * 2:
        return msgs
    # Keep system plus tail of base
    system = [m for m in msgs if m["role"] == "system"][:1]
    tail = base[-MAX_HISTORY*2:]
    return system + tail

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    user_text = (request.values.get("Body") or "").strip()
    wa_from = request.values.get("From", "")  # e.g., whatsapp:+91...

    sess = session_for(wa_from)

    # Build/ensure system prompt
    system_msg = {"role": "system", "content": build_system_prompt(BOT_WHATSAPP_NUMBER, BOT_FIRST_CODE)}
    if not any(m.get("role") == "system" for m in sess["messages"]):
        sess["messages"].insert(0, system_msg)

    # If this is the first assistant reply ever for this number, we pass a hint token
    if not sess["sent_header"]:
        # Add a one-time assistant 'tool' hint so the model knows it's first reply
        sess["messages"].append({"role": "system", "content": "First assistant reply in this conversation: include header."})

    # Add user message
    sess["messages"].append({"role": "user", "content": user_text})
    sess["messages"] = trim_history(sess["messages"])

    # Get AI reply
    try:
        ai_text = chat_completion(sess["messages"])
    except Exception as e:
        # Fallback minimal reply
        ai_text = (
            f"📞 WhatsApp: {BOT_WHATSAPP_NUMBER}\n🔑 Code: {BOT_FIRST_CODE}\n"
            "Thanks for reaching out! Could you tell me your business type and city?"
            if not sess["sent_header"] else
            "Thanks! Please share your business type and city so I can plan a quick demo."
        )

    # After first successful assistant message, mark header sent
    if not sess["sent_header"]:
        sess["sent_header"] = True

    # Save assistant message to history
    sess["messages"].append({"role": "assistant", "content": ai_text})
    sess["messages"] = trim_history(sess["messages"])

    # Return to Twilio
    resp = MessagingResponse()
    resp.message(ai_text)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
