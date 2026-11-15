import logging

from fastapi import APIRouter, HTTPException
from langgraph.errors import GraphRecursionError

from app.agents.assistant import run_agent
from app.schemas.agents import AgentRequest, AgentResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/assistant/run", response_model=AgentResponse)
def run_assistant(body: AgentRequest):
    try:
        return run_agent(body.message)
    except GraphRecursionError:
        raise HTTPException(status_code=500, detail="Agent stopped: too many steps")
    except Exception:
        logger.exception("Agent run failed")
        raise HTTPException(status_code=502, detail="The agent request failed")