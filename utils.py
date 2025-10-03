import re, csv, os, datetime

LOG_PATH = os.getenv("LEAD_LOG_PATH", "leads.csv")

BUSINESS_HINTS = [
    "store","clinic","service","hospital","shop","salon","ecom","ecommerce","toys","agriculture",
    "education","restaurant","cafe","hotel","gym","real estate","agency","travel","pharmacy"
]
LOCATION_HINTS = [
    "kerala","kochi","ernakulam","thrissur","calicut","malappuram","trivandrum","kannur",
    "mumbai","delhi","bangalore","bengaluru","chennai","hyderabad","kolkata","pune","ahmedabad"
]

def guess(tag_list, text):
    t = text.lower()
    hit = [w for w in tag_list if w in t]
    return ", ".join(sorted(set(hit))) if hit else ""

def log_lead(phone, user_text, ai_text):
    os.makedirs(os.path.dirname(LOG_PATH) or ".", exist_ok=True)
    exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["time","phone","user_text","ai_text","business_guess","location_guess"])
        w.writerow([datetime.datetime.utcnow().isoformat(), phone, user_text, ai_text, guess(BUSINESS_HINTS, user_text), guess(LOCATION_HINTS, user_text)])
