import os
from dotenv import load_dotenv
from datetime import datetime
from db import load_events
from scheduler import Scheduler
from utils import send_email

load_dotenv()
scheduler = Scheduler()
events = load_events()

# Filter today's events
today = datetime.now().date()
today_events = [e for e in events if e.start_time.date() == today]

if not today_events:
    print("No events for today.")
    exit()

agenda_text = "\n".join([
    f"{e.title} - {e.start_time.strftime('%I:%M %p')} → {e.end_time.strftime('%I:%M %p')}\n{e.description}"
    for e in today_events
])

subject = f"📅 Your Campus Copilot Agenda for {today.strftime('%B %d')}"
receivers = os.getenv("DAILY_EMAIL_RECEIVERS").split(",")

for recipient in receivers:
    success = send_email(recipient.strip(), subject, agenda_text)
    if success:
        print(f"✅ Sent to {recipient}")
    else:
        print(f"❌ Failed to send to {recipient}")