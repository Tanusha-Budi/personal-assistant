from googleapiclient.discovery import build

from app.services.google_auth import get_credentials


def search_messages(query: str, max_results: int = 10) -> list[dict]:
    service = build("gmail", "v1", credentials=get_credentials())

    listing = service.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()

    messages = []
    for ref in listing.get("messages", []):
        msg = service.users().messages().get(
            userId="me",
            id=ref["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"],
        ).execute()
        messages.append(msg)
    return messages