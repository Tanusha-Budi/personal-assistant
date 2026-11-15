from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from googleapiclient.discovery import build

from app.config import settings
from app.services.google_auth import get_credentials


def list_events_for_day(day) -> list[dict]:
    tz = ZoneInfo(settings.timezone)
    start = datetime.combine(day, time.min, tzinfo=tz)
    end = start + timedelta(days=1)

    service = build("calendar", "v3", credentials=get_credentials())
    result = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    return result.get("items", [])