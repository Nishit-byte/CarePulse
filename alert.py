import os
import time
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
TWILIO_TO = os.getenv("TWILIO_WHATSAPP_TO")

def send_whatsapp_alert(location="Living Room"):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    timestamp = time.strftime("%I:%M %p")
    body = (
        f"Emergency Alert\n"
        f"A possible fall has been detected.\n"
        f"Time: {timestamp}\n"
        f"Location: {location}\n"
        f"Please check on the person immediately."
    )
    client.messages.create(body=body, from_=TWILIO_FROM, to=TWILIO_TO)
    return timestamp