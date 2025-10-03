import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from ai import build_system_prompt, chat_completion

app = Flask(__name__)

# Config
BOT_WHATSAPP_NUMBER = os.getenv("BOT_WHATSAPP_NUMBER", "+14155238886")
BOT_FIRST_CODE = os.getenv("BOT_FIRST_CODE", "THRYVIX2025")
MAX_HISTORY = int(os.getenv("MAX_HISTORY", "6"))  # messages per role to keep

# Store conversations in memory: { phone: {"messages": [], "sent_header": False} }
SESSIONS = {}

def session_for(phone: str):
    if phone not in SESSIONS:
        SESSIONS[phone] = {"messages": [], "sent_header": False}
    return SESSIONS[phone]

def trim_history(msgs):
    """Keep only last MAX_HISTORY*2 user+assistant messages, plus system."""
    system = [m for m in msgs if m["role"] == "system"]
    base = [m for m in msgs if m["role"] != "system"]
    if len(base) <= MAX_HISTORY * 2:
        return system + base
    return system + base[-MAX_HISTORY*2:]

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    user_text = (request.values.get("Body") or "").strip()
    wa_from = request.values.get("From", "")  # e.g. whatsapp:+91XXXXXXXXXX

    sess = session_for(wa_from)

    # Ensure system message exists
    if not any(m["role"] == "system" for m in sess["messages"]):
        system_msg = {"role": "system", "content": build_system_prompt(BOT_WHATSAPP_NUMBER, BOT_FIRST_CODE)}
        sess["messages"].insert(0, system_msg)

    # Track first reply header injection
    if not sess["sent_header"]:
        sess["messages"].append({"role": "system", "content": "First assistant reply: include WhatsApp number and code header."})

    # Add user input
    sess["messages"].append({"role": "user", "content": user_text})
    sess["messages"] = trim_history(sess["messages"])

    # Get AI reply
    try:
        ai_text = chat_completion(sess["messages"])
    except Exception as e:
        ai_text = (
            f"📞 WhatsApp: {BOT_WHATSAPP_NUMBER}\n🔑 Code: {BOT_FIRST_CODE}\n"
            "Thanks for reaching out! Could you share your business type and city?"
            if not sess["sent_header"]
            else "Thanks! Please share your business type and city so we can plan a demo."
        )

    # Mark header as sent after first assistant message
    if not sess["sent_header"]:
        sess["sent_header"] = True

    # Save assistant reply
    sess["messages"].append({"role": "assistant", "content": ai_text})
    sess["messages"] = trim_history(sess["messages"])

    # Reply to Twilio
    resp = MessagingResponse()
    resp.message(ai_text)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
