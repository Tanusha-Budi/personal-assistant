import json
from datetime import date

from langchain_core.tools import tool

from app.tools import calendar_tools, gmail_tools, github_tools


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


@tool
def search_gmail(query: str = "newer_than:1d", max_results: int = 10) -> str:
    """Search the user's Gmail and return sender, subject, date and a short
    snippet for each matching email.

    Use this when the user asks about their emails, such as unread mail,
    messages from a person, or messages about a topic.

    Args:
        query: A Gmail search query, for example "is:unread", "from:alex@example.com",
            "subject:invoice" or "newer_than:2d". Defaults to the last day.
        max_results: How many emails to return, from 1 to 20.
    """
    try:
        emails = gmail_tools.search_emails(query, max_results)
    except Exception as e:
        return f"Gmail search failed: {e}"

    if not emails:
        return f"No emails found for: {query}"
    return json.dumps([e.model_dump() for e in emails])

@tool
def list_github_repos(limit: int = 10) -> str:
    """List the user's GitHub repositories, most recently updated first.

    Use this to find the exact repository name before asking about its issues
    or pull requests.

    Args:
        limit: How many repositories to return, from 1 to 20.
    """
    try:
        repos = github_tools.get_repos(limit)
    except Exception as e:
        return f"GitHub lookup failed: {e}"
    if not repos:
        return "No repositories found."
    return json.dumps([r.model_dump() for r in repos])


@tool
def list_github_issues(repo: str, state: str = "open", limit: int = 10) -> str:
    """List issues in one GitHub repository. Pull requests are not included.

    Use this when the user asks about issues, bugs or tasks in a repository.

    Args:
        repo: The repository in 'owner/name' format, for example 'octocat/hello'.
            If unsure of the name, call list_github_repos first.
        state: 'open', 'closed' or 'all'. Defaults to 'open'.
        limit: How many issues to return, from 1 to 20.
    """
    try:
        issues = github_tools.get_issues(repo, state, limit)
    except Exception as e:
        return f"GitHub lookup failed: {e}"
    if not issues:
        return f"No {state} issues in {repo}."
    return json.dumps([i.model_dump() for i in issues])


@tool
def list_github_pull_requests(repo: str, state: str = "open", limit: int = 10) -> str:
    """List pull requests in one GitHub repository.

    Use this when the user asks about pull requests, PRs or code reviews.

    Args:
        repo: The repository in 'owner/name' format. If unsure of the name,
            call list_github_repos first.
        state: 'open', 'closed' or 'all'. Defaults to 'open'.
        limit: How many pull requests to return, from 1 to 20.
    """
    try:
        pulls = github_tools.get_pull_requests(repo, state, limit)
    except Exception as e:
        return f"GitHub lookup failed: {e}"
    if not pulls:
        return f"No {state} pull requests in {repo}."
    return json.dumps([p.model_dump() for p in pulls])