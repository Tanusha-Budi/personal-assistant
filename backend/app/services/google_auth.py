from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from app.config import settings

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.readonly",
]


def get_credentials() -> Credentials:
    creds = Credentials.from_authorized_user_file(settings.google_token_path, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(settings.google_token_path, "w") as f:
            f.write(creds.to_json())
    return creds