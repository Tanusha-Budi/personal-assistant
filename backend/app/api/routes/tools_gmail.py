from fastapi import APIRouter

from app.schemas.emails import EmailSummary
from app.tools import gmail_tools

router = APIRouter(prefix="/tools/gmail", tags=["tools"])


@router.get("/search", response_model=list[EmailSummary])
def search(query: str = "newer_than:1d", max_results: int = 10):
    return gmail_tools.search_emails(query, max_results)