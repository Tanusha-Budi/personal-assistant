from app.api.routes import tools_calendar
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, tools_calendar, tools_gmail, tools_github, agents
from app.config import settings

import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.logging import request_id_var, setup_logging

request_logger = logging.getLogger("app.request")


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title=settings.app_name)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        request_id = uuid.uuid4().hex[:8]
        token = request_id_var.set(request_id)
        started = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            request_logger.exception("%s %s crashed", request.method, request.url.path)
            request_id_var.reset(token)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error", "request_id": request_id},
            )
        elapsed_ms = (time.perf_counter() - started) * 1000
        request_logger.info(
            "%s %s -> %d (%.0f ms)",
            request.method, request.url.path, response.status_code, elapsed_ms,
        )
        response.headers["X-Request-ID"] = request_id
        request_id_var.reset(token)
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_origin],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"]
    )

    app.include_router(health.router, prefix="/api")
    app.include_router(tools_calendar.router, prefix="/api")
    app.include_router(tools_gmail.router, prefix="/api")
    app.include_router(tools_github.router, prefix="/api")
    app.include_router(agents.router, prefix="/api")
    return app


app = create_app()