import uuid

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph import MessagesState


def _call(name: str, args: dict) -> AIMessage:
    return AIMessage(
        content="",
        tool_calls=[{"name": name, "args": args, "id": f"call_{uuid.uuid4().hex[:8]}"}],
    )


def fake_call_model(state: MessagesState):
    last = state["messages"][-1]

    if isinstance(last, ToolMessage):
        preview = str(last.content)[:200]
        return {"messages": [AIMessage(content=f"(fake model) Tool returned: {preview}")]}

    text = last.content.lower() if isinstance(last, HumanMessage) else ""
    if "calendar" in text or "meeting" in text:
        return {"messages": [_call("get_calendar_events", {})]}
    if "email" in text or "mail" in text:
        return {"messages": [_call("search_gmail", {"query": "newer_than:1d", "max_results": 3})]}
    if "github" in text or "repo" in text:
        return {"messages": [_call("list_github_repos", {"limit": 3})]}
    return {"messages": [AIMessage(content="(fake model) I can help with calendar, email or GitHub.")]}