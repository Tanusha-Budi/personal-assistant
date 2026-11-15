import logging
import re
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import settings

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")

_SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_\-]+"),
    re.compile(r"github_pat_[A-Za-z0-9_]+"),
    re.compile(r"ghp_[A-Za-z0-9]+"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]+"),
]


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


class RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        text = super().format(record)
        for pattern in _SECRET_PATTERNS:
            text = pattern.sub("[REDACTED]", text)
        return text


def setup_logging() -> None:
    formatter = RedactingFormatter(
        "%(asctime)s | %(levelname)-7s | %(request_id)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if settings.log_to_file:
        Path(settings.log_dir).mkdir(parents=True, exist_ok=True)
        handlers.append(
            RotatingFileHandler(
                Path(settings.log_dir) / "app.log",
                maxBytes=1_000_000,
                backupCount=3,
                encoding="utf-8",
            )
        )

    for handler in handlers:
        handler.setFormatter(formatter)
        handler.addFilter(RequestIdFilter())

    logging.basicConfig(level=logging.WARNING, handlers=handlers, force=True)
    logging.getLogger("app").setLevel(settings.log_level)

    for noisy in ("httpx", "httpx2", "httpcore", "googleapiclient"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)