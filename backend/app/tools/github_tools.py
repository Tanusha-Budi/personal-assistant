from app.schemas.github import IssueSummary, PullRequestSummary, RepoSummary
from app.services import github

ALLOWED_STATES = {"open", "closed", "all"}


def _clean_state(state: str) -> str:
    if state not in ALLOWED_STATES:
        raise ValueError("state must be one of: open, closed, all")
    return state


def _clean_limit(limit: int) -> int:
    return max(1, min(limit, 20))


def get_repos(limit: int = 10) -> list[RepoSummary]:
    items = github.list_repos(_clean_limit(limit))
    return [
        RepoSummary(
            full_name=r["full_name"],
            description=r.get("description"),
            private=r["private"],
            updated_at=r["updated_at"],
            url=r["html_url"],
        )
        for r in items
    ]


def get_issues(repo: str, state: str = "open", limit: int = 10) -> list[IssueSummary]:
    state = _clean_state(state)
    limit = _clean_limit(limit)
    items = github.list_issues(repo, state)

    issues = []
    for i in items:
        if "pull_request" in i:      # GitHub's issues endpoint also returns pull requests
            continue
        issues.append(
            IssueSummary(
                number=i["number"],
                title=i["title"],
                state=i["state"],
                author=i["user"]["login"],
                labels=[label["name"] for label in i.get("labels", [])],
                updated_at=i["updated_at"],
                url=i["html_url"],
            )
        )
        if len(issues) == limit:
            break
    return issues


def get_pull_requests(repo: str, state: str = "open", limit: int = 10) -> list[PullRequestSummary]:
    state = _clean_state(state)
    items = github.list_pull_requests(repo, state, _clean_limit(limit))
    return [
        PullRequestSummary(
            number=p["number"],
            title=p["title"],
            state=p["state"],
            author=p["user"]["login"],
            draft=p.get("draft", False),
            updated_at=p["updated_at"],
            url=p["html_url"],
        )
        for p in items
    ]