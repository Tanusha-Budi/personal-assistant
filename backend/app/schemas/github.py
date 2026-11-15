from pydantic import BaseModel


class RepoSummary(BaseModel):
    full_name: str
    description: str | None = None
    private: bool
    updated_at: str
    url: str


class IssueSummary(BaseModel):
    number: int
    title: str
    state: str
    author: str
    labels: list[str]
    updated_at: str
    url: str


class PullRequestSummary(BaseModel):
    number: int
    title: str
    state: str
    author: str
    draft: bool
    updated_at: str
    url: str