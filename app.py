import os, traceback
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from ai import SYSTEM_PROMPT, chat_completion
from utils import log_lead

app = Flask(__name__)

MAX_TURNS = 6  # user+assistant pairs to keep
sessions = {}  # phone -> [{"role":..., "content":...}, ...]

def get_history(phone):
    if phone not in sessions:
        sessions[phone] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return sessions[phone]

def trim(history):
    sys = [m for m in history if m["role"] == "system"][:1]
    rest = [m for m in history if m["role"] != "system"]
    tail = rest[-2*MAX_TURNS:]
    return sys + tail

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    phone = request.values.get("From", "")
    text = (request.values.get("Body") or "").strip()
    history = get_history(phone)
    history.append({"role": "user", "content": text})
    history[:] = trim(history)

    try:
        ai_text = chat_completion(history)
        history.append({"role": "assistant", "content": ai_text})
        history[:] = trim(history)
    except Exception as e:
        traceback.print_exc()
        ai_text = "Thanks! Could you tell me your business type and city so I can plan a quick demo?"

    try:
        log_lead(phone, text, ai_text)
    except Exception:
        traceback.print_exc()

    resp = MessagingResponse()
    resp.message(ai_text)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
