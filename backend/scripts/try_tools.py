# from app.tools.langchain_tools import get_calendar_events

# print("NAME:", get_calendar_events.name)
# print("DESCRIPTION:", get_calendar_events.description)
# print("ARGS:", get_calendar_events.args)
# print("RESULT:", get_calendar_events.invoke({"day": "2026-11-14"}))


# from app.tools.langchain_tools import search_gmail

# print("NAME:", search_gmail.name)
# print("ARGS:", search_gmail.args)
# result = search_gmail.invoke({"query": "newer_than:7d", "max_results": 3})
# print("RESULT:", result)

from app.tools.langchain_tools import (
    list_github_issues,
    list_github_pull_requests,
    list_github_repos,
)

print("REPOS:", list_github_repos.invoke({"limit": 5}))
print("ISSUES:", list_github_issues.invoke({"repo": "Tanusha-Budi/personal-assistant"}))
print("PRS:", list_github_pull_requests.invoke({"repo": "Tanusha-Budi/personal-assistant"}))
print("BAD REPO:", list_github_issues.invoke({"repo": "not a repo"}))