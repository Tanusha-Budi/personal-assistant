from app.schemas.emails import EmailSummary
from app.services import google_gmail


def search_emails(query: str, max_results: int = 10) -> list[EmailSummary]:
    max_results = max(1, min(max_results, 20))
    items = google_gmail.search_messages(query, max_results)

    results = []
    for m in items:
        headers = {h["name"].lower(): h["value"] for h in m["payload"]["headers"]}
        results.append(
            EmailSummary(
                id=m["id"],
                sender=headers.get("from", ""),
                subject=headers.get("subject", "(no subject)"),
                date=headers.get("date", ""),
                snippet=m.get("snippet", ""),
            )
        )
    return results