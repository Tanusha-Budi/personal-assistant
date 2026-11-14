from datetime import date

from fastapi import APIRouter

from app.schemas.events import CalendarEvent
from app.tools import calendar_tools

router = APIRouter(prefix="/tools/calendar", tags=["tools"])


@router.get("/events", response_model=list[CalendarEvent])
def events(day: date | None = None):
    return calendar_tools.get_events(day or date.today())