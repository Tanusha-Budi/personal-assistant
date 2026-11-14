import json
from datetime import date

from langchain_core.tools import tool

from app.tools import calendar_tools


@tool
def get_calendar_events(day: str | None = None) -> str:
    """Get the user's Google Calendar events for one day.

    Use this when the user asks what is on their calendar, what meetings they
    have, or whether they are free at a certain time.

    Args:
        day: The date in YYYY-MM-DD format. If omitted, today is used.
    """
    try:
        target = date.fromisoformat(day) if day else date.today()
    except ValueError:
        return "Invalid date. Use the format YYYY-MM-DD."

    try:
        events = calendar_tools.get_events(target)
    except Exception as e:
        return f"Calendar lookup failed: {e}"

    if not events:
        return f"No events on {target.isoformat()}."
    return json.dumps([e.model_dump() for e in events])