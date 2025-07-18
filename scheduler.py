from datetime import datetime, timedelta
from events import Event

class Scheduler:
    def get_schedule(self):
        return [
            "📬 Daily agenda email at 8:00 AM (via SendGrid)",
            "🗓️ View your 3-day event agenda here"
        ]

    def get_upcoming_agenda(self, events, days=3):
        today = datetime.now().date()
        upcoming = []
        for e in events:
            delta = (e.start_time.date() - today).days
            if 0 <= delta <= days:
                upcoming.append(e)
        return sorted(upcoming, key=lambda x: x.start_time)
