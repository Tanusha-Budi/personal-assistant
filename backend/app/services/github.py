import re

import httpx

from app.config import settings

BASE_URL = "https://api.github.com"
REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def _client() -> httpx.Client:
    return httpx.Client(
        base_url=BASE_URL,
        headers={
            "Authorization": f"Bearer {settings.github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=10,
    )


def _check_repo(repo: str) -> str:
    if not REPO_PATTERN.match(repo):
        raise ValueError("repo must look like 'owner/name'")
    return repo


def list_repos(limit: int = 10) -> list[dict]:
    with _client() as client:
        r = client.get("/user/repos", params={"sort": "updated", "per_page": limit})
        r.raise_for_status()
        return r.json()


def list_issues(repo: str, state: str = "open", per_page: int = 30) -> list[dict]:
    repo = _check_repo(repo)
    with _client() as client:
        r = client.get(f"/repos/{repo}/issues", params={"state": state, "per_page": per_page})
        r.raise_for_status()
        return r.json()


def list_pull_requests(repo: str, state: str = "open", per_page: int = 10) -> list[dict]:
    repo = _check_repo(repo)
    with _client() as client:
        r = client.get(f"/repos/{repo}/pulls", params={"state": state, "per_page": per_page})
        r.raise_for_status()
        return r.json()