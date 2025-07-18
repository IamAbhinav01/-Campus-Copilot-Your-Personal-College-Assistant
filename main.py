import streamlit as st
from dotenv import load_dotenv
from events import Event, EventManager, format_event
from db import load_events, save_events, delete_event_by_title
from scheduler import Scheduler
from assistant import Assistant
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
import os
from streamlit_lottie import st_lottie
import json
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def main():
    load_dotenv()
    lottie_animation = load_lottie_file("lottieflow-attention-09-000000-easey.json")
    
    st.set_page_config(page_title="Campus Copilot", layout="wide")
    st.markdown("""
    <style>
    /* Hide Streamlit default footer and hamburger menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* App-wide font */
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
    }

    /* Title */
    h1 {
        text-align: center;
        color: #6f42c1;
    }

    /* Section Headers */
    h2, h3 {
        color: #5a32a3;
        margin-top: 20px;
        border-bottom: 2px solid #eee;
        padding-bottom: 6px;
    }

    /* Cards */
    .stMarkdown {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }

    /* Buttons */
    button[kind="primary"] {
        background-color: #6f42c1;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 18px;
        font-weight: 600;
    }

    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

    if "user_email" not in st.session_state:
        st.session_state.user_email = None

    # ✅ Top Nav Menu
    selected = option_menu(
        menu_title=None,
        options=["Home", "Events", "Schedule", "Calendar", "Assistant", "Logout"],
        icons=["house", "calendar", "alarm", "calendar3", "robot", "box-arrow-right"],
        orientation="horizontal",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "icon": {"color": "#6f42c1", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px"},
            "nav-link-selected": {"background-color": "#e8ddf7"},
        },
    )

    st.markdown("<h1 style='text-align: center;'>🎓 Campus Copilot</h1>", unsafe_allow_html=True)

    # ✅ Login Section
    if not st.session_state.user_email:
        st.markdown("### 🔐 Please login to continue")
        email_input = st.text_input("Enter your email")
        if st.button("Login") and email_input:
            st.session_state.user_email = email_input
            st.rerun()
        st.stop()

    # 🔄 Load user data
    event_manager = EventManager()
    scheduler = Scheduler()
    assistant = Assistant()

    try:
        event_manager.events = load_events(st.session_state.user_email)
    except Exception as e:
        st.error(f"❌ Error loading events: {e}")
        return

    # 🏠 Home
    if selected == "Home":
        col1, col2 = st.columns(2)

        with col1:
            st_lottie(lottie_animation, speed=1, height=300, key="copilot-hero")

        with col2:
            st.markdown("### 👋 Welcome to **Campus Copilot**")
            st.write("Your personal college assistant to manage classes, events, and reminders with ease.")
            st.success("💡 Pro Tip: Use the Assistant tab to ask anything about your schedule!")

    # 📆 Calendar View
    elif selected == "Calendar":
        from streamlit_calendar import calendar
        st.subheader("📆 Your Event Calendar")

        events_data = [
            {
                "title": f"{event.title} ({event.category})",
                "start": event.start_time.isoformat(),
                "end": event.end_time.isoformat(),
            }
            for event in event_manager.get_events()
        ]
        calendar_options = {
            "initialView": "dayGridMonth",
            "editable": False,
            "height": 650,
        }
        calendar(events=events_data, options=calendar_options)

    # 📋 Events
    elif selected == "Events":
        st.subheader("🔍 Search Events")
        search_query = st.text_input("Search by title or description")
        selected_category = st.selectbox("Filter by Category", ["All", "Class", "Club", "Exam", "Assignment", "Other"])

        filtered = [
            event for event in event_manager.get_events()
            if (search_query.lower() in event.title.lower() or search_query.lower() in event.description.lower())
            and (selected_category == "All" or event.category == selected_category)
        ]

        st.subheader("📅 Current Events")
        if not filtered:
            st.info("No events found.")
        else:
            for event in filtered:
                st.markdown(f"- {format_event(event)}")

        # ➕ Add
        st.markdown("---")
        st.subheader("➕ Add Event")
        title = st.text_input("Title")
        description = st.text_area("Description")
        category = st.selectbox("Category", ["Class", "Club", "Exam", "Assignment", "Other"])
        now = datetime.now()
        start_date = st.date_input("Start Date", value=now.date())
        start_time = st.time_input("Start Time", value=now.time())
        end_date = st.date_input("End Date", value=now.date())
        end_time = st.time_input("End Time", value=(now + timedelta(hours=1)).time())
        
        if st.button("Add Event"):
            new_event = Event(title, description,
                              datetime.combine(start_date, start_time),
                              datetime.combine(end_date, end_time),
                              category)
            event_manager.add_event(new_event)
            save_events(event_manager.get_events(), st.session_state.user_email)
            st.success("✅ Event added!")
            st.rerun()

        # 🗑️ Delete
        st.subheader("🗑️ Delete Event")
        titles = [e.title for e in event_manager.get_events()]
        if titles:
            selected_title = st.selectbox("Select event to delete", titles)
            if st.button("Delete"):
                delete_event_by_title(selected_title, st.session_state.user_email)
                st.success("✅ Deleted.")
                st.rerun()
        else:
            st.info("No events to delete.")

    # 🕒 Schedule
    elif selected == "Schedule":
        st.subheader("📌 Next 3 Days")
        agenda = scheduler.get_upcoming_agenda(event_manager.get_events(), days=3)
        if not agenda:
            st.info("No upcoming events.")
        else:
            for event in agenda:
                st.markdown(f"- {format_event(event)}")

        st.markdown("### 📩 Email Agenda")
        email_to = st.text_input("Your Email")
        if st.button("Send Agenda"):
            from utils import send_email
            text = "\n".join([f"{e.title}: {e.start_time.strftime('%Y-%m-%d %H:%M')}" for e in agenda])
            if send_email(email_to, "Your Agenda", text):
                st.success("✅ Sent successfully!")
            else:
                st.error("❌ Failed to send.")

    # 🤖 Assistant
    elif selected == "Assistant":
        st.subheader("🤖 Ask Campus Copilot")
        query = st.text_input("Ask something...")
        if st.button("Ask"):
            response = assistant.run(query, event_manager.get_events())
            st.markdown("### 🧠 Response")
            st.write(response)

    # 🚪 Logout
    elif selected == "Logout":
        st.session_state.clear()
        st.success("✅ Logged out.")
        st.stop()

if __name__ == "__main__":
    main()
