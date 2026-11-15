import httpx
from fastapi import APIRouter, HTTPException

from app.schemas.github import IssueSummary, PullRequestSummary, RepoSummary
from app.tools import github_tools

router = APIRouter(prefix="/tools/github", tags=["tools"])


def _handle(e: Exception) -> HTTPException:
    if isinstance(e, ValueError):
        return HTTPException(status_code=400, detail=str(e))
    if isinstance(e, httpx.HTTPStatusError):
        code = e.response.status_code
        if code == 404:
            return HTTPException(status_code=404, detail="Repository not found or not accessible")
        return HTTPException(status_code=502, detail="GitHub request failed")
    return HTTPException(status_code=500, detail="Unexpected error")


@router.get("/repos", response_model=list[RepoSummary])
def repos(limit: int = 10):
    try:
        return github_tools.get_repos(limit)
    except Exception as e:
        raise _handle(e)


@router.get("/issues", response_model=list[IssueSummary])
def issues(repo: str, state: str = "open", limit: int = 10):
    try:
        return github_tools.get_issues(repo, state, limit)
    except Exception as e:
        raise _handle(e)


@router.get("/pulls", response_model=list[PullRequestSummary])
def pulls(repo: str, state: str = "open", limit: int = 10):
    try:
        return github_tools.get_pull_requests(repo, state, limit)
    except Exception as e:
        raise _handle(e)