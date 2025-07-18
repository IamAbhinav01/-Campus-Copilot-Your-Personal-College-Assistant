import os
from dotenv import load_dotenv
from astrapy import DataAPIClient
from events import Event
from datetime import datetime

# Load environment variables
load_dotenv()

API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
COLLECTION_NAME = os.getenv("ASTRA_DB_COLLECTION")

# Connect to Astra DB
client = DataAPIClient(TOKEN)
db = client.get_database_by_api_endpoint(API_ENDPOINT)
collection = db.get_collection(COLLECTION_NAME)

# Save a single event for a user
def save_event(event: Event, user_email: str):
    document = {
        "title": event.title,
        "description": event.description,
        "start_time": event.start_time.isoformat(),
        "end_time": event.end_time.isoformat(),
        "category": event.category,
        "user_email": user_email
    }
    collection.insert_one(document)

# Overwrite all events for a user (optional, useful on update)
def save_events(events, user_email):
    collection.delete_many({"user_email": user_email})
    for event in events:
        save_event(event, user_email)

# Load all events for a specific user
def load_events(user_email: str):
    documents = collection.find({"user_email": user_email})
    events = []
    for doc in documents:
        events.append(Event(
            title=doc["title"],
            description=doc["description"],
            start_time=datetime.fromisoformat(doc["start_time"]),
            end_time=datetime.fromisoformat(doc["end_time"]),
            category=doc.get("category", "General")
        ))
    return events

# Delete a single event by title (for current user)
def delete_event_by_title(title, user_email: str):
    collection.delete_one({"title": title, "user_email": user_email})
