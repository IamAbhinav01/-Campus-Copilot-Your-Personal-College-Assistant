from datetime import datetime

class Event:
    def __init__(self, title, description, start_time, end_time, category="General"):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.category = category

    def __str__(self):
        return f"[{self.category}] {self.title}: {self.start_time} - {self.end_time}"

class EventManager:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        self.events.remove(event)

    def get_events(self):
        return self.events

    def get_events_on_date(self, date):
        return [event for event in self.events if event.start_time.date() == date]

def format_event(event):
    return f"**{event.title}** - {event.start_time.strftime('%Y-%m-%d %H:%M')} → {event.end_time.strftime('%Y-%m-%d %H:%M')}  \n_{event.description}_"
