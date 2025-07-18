import os
import requests

def send_email(to_email, subject, body):
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL")

    data = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": FROM_EMAIL},
        "subject": subject,
        "content": [{"type": "text/plain", "value": body}]
    }

    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {SENDGRID_API_KEY}",
            "Content-Type": "application/json"
        },
        json=data
    )

    if response.status_code != 202:
        print("Error sending email:", response.text)

    return response.status_code == 202
