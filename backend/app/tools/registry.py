from app.tools.langchain_tools import (
    get_calendar_events,
    list_github_issues,
    list_github_pull_requests,
    list_github_repos,
    search_gmail,
)

READ_TOOLS = [
    get_calendar_events,
    search_gmail,
    list_github_repos,
    list_github_issues,
    list_github_pull_requests,
]