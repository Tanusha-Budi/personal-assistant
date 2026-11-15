from pydantic import BaseModel


class EmailSummary(BaseModel):
    id: str
    sender: str
    subject: str
    date: str
    snippet: str