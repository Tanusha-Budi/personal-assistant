from pydantic import BaseModel


class CalendarEvent(BaseModel):
    id: str
    title: str
    start: str
    end: str
    location: str | None = None