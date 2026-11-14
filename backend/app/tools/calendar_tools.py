from datetime import date

from app.schemas.events import CalendarEvent
from app.services import google_calendar


def get_events(day: date) -> list[CalendarEvent]:
    items = google_calendar.list_events_for_day(day)
    events = []
    for item in items:
        start = item["start"].get("dateTime") or item["start"].get("date")
        end = item["end"].get("dateTime") or item["end"].get("date")
        events.append(
            CalendarEvent(
                id=item["id"],
                title=item.get("summary", "(no title)"),
                start=start,
                end=end,
                location=item.get("location"),
            )
        )
    return events