# Thryvix AI Lead Bot — Full AI Mode (Free Stack)

WhatsApp bot for leads that replies **in real time** using **OpenAI API**, runs 24×7 on **Render**, and receives messages via **Twilio WhatsApp Sandbox/number**.

## Features
- First reply includes your **WhatsApp number** and **code** automatically
- Real-time AI replies using OpenAI (no preset trees)
- Detects user style/language (English, Malayalam/Hindi script, or Manglish/Hinglish) and mirrors it
- Keeps short context per phone number for better continuity
- Graceful fallback replies if AI fails

---
## 1) Environment Variables (Render → Settings → Environment)
- `OPENAI_API_KEY` = your OpenAI key (starts with `sk-...`)
- `OPENAI_MODEL` = gpt-4o-mini  (or another chat-capable model you have access to)
- `BOT_WHATSAPP_NUMBER` = your Twilio sandbox number or WA-enabled number (e.g., +14155238886)
- `BOT_FIRST_CODE` = the code you want to show in first message (e.g., THRYVIX2025)
- `MAX_HISTORY` = 6   (optional; number of past messages to keep per user)

---
## 2) Deploy on Render (Free)
- New Web Service → Connect your GitHub repo (or upload these files)
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Add all environment variables above
- Copy the Render URL (e.g., `https://your-service.onrender.com`)

---
## 3) Configure Twilio Sandbox
- Twilio Console → Messaging → Try it out → WhatsApp Sandbox
- In “WHEN A MESSAGE COMES IN” set:
  `https://YOUR-RENDER-URL/whatsapp`
- Join the sandbox from your phone and send a test message

---
## 4) Local Testing (optional)
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o-mini
export BOT_WHATSAPP_NUMBER=+14155238886
export BOT_FIRST_CODE=THRYVIX2025
flask --app app run --host=0.0.0.0 --port=5000
```
Use ngrok to expose locally:
```bash
ngrok http 5000
```
Set Twilio webhook to `https://NGROK_URL/whatsapp`

---
## Notes
- This demo keeps conversation state **in memory**. On restart, it resets.
- For production, connect a database or Google Sheets.
