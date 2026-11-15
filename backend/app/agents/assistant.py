from functools import lru_cache

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.agents.fake_model import fake_call_model
from app.agents.prompts import system_prompt
from app.config import settings
from app.tools.registry import READ_TOOLS

import logging
import time

logger = logging.getLogger(__name__)


def _real_model_node():
    from langchain_anthropic import ChatAnthropic

    model = ChatAnthropic(
        model=settings.llm_model,
        api_key=settings.anthropic_api_key,
        max_tokens=settings.llm_max_tokens
    ).bind_tools(READ_TOOLS)

    def call_model(state: MessagesState):
        messages = [SystemMessage(content=system_prompt())] + state["messages"]
        return {"messages": [model.invoke(messages)]}

    return call_model


@lru_cache
def get_graph():
    call_model = fake_call_model if settings.llm_provider == "fake" else _real_model_node()

    builder = StateGraph(MessagesState)
    builder.add_node("agent", call_model)
    builder.add_node("tools", ToolNode(READ_TOOLS))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    return builder.compile()


def _text(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(
        block.get("text", "") for block in content if isinstance(block, dict)
    )


# def run_agent(message: str) -> dict:
#     result = get_graph().invoke(
#         {"messages": [HumanMessage(content=message)]},
#         config={"recursion_limit": settings.agent_recursion_limit},
#     )
#     messages = result["messages"]

#     tool_calls = []
#     usage = {"input_tokens": 0, "output_tokens": 0}
#     for m in messages:
#         if isinstance(m, AIMessage):
#             for c in m.tool_calls:
#                 tool_calls.append({"name": c["name"], "args": c["args"]})
#             if m.usage_metadata:
#                 usage["input_tokens"] += m.usage_metadata.get("input_tokens", 0)
#                 usage["output_tokens"] += m.usage_metadata.get("output_tokens", 0)

#     return {
#         "answer": _text(messages[-1].content),
#         "tool_calls": tool_calls,
#         "usage": usage,
#     }


def run_agent(message: str) -> dict:
    tool_calls = []
    usage = {"input_tokens": 0, "output_tokens": 0}
    final_answer = ""

    started = time.perf_counter()
    logger.info("agent run started (message length=%d)", len(message))
    logger.debug("user message: %s", message)

    graph = get_graph()

    try:
        for step in graph.stream(
            {"messages": [HumanMessage(content=message)]},
            config={"recursion_limit": settings.agent_recursion_limit},
            stream_mode="updates",
        ):
            for node_name, update in step.items():
                messages = (update or {}).get("messages", [])

                for m in messages:

                    if isinstance(m, AIMessage):
                        for c in m.tool_calls:
                            logger.info(
                                "  -> tool call from %s: %s (args: %s)",
                                node_name,
                                c["name"],
                                list(c["args"].keys()),
                            )

                            logger.debug("  -> tool args: %s", c["args"])

                            tool_calls.append({
                                "node": node_name,
                                "name": c["name"],
                                "args": c["args"],
                            })

                        if not m.tool_calls:
                            final_answer = _text(m.content)

                        if m.usage_metadata:
                            usage["input_tokens"] += m.usage_metadata.get(
                                "input_tokens", 0
                            )
                            usage["output_tokens"] += m.usage_metadata.get(
                                "output_tokens", 0
                            )

                    elif isinstance(m, ToolMessage):
                        logger.info(
                            "  <- tool result from %s: %s (%d chars)",
                            node_name,
                            m.name,
                            len(str(m.content)),
                        )

                        logger.debug(
                            "  <- tool result: %s",
                            str(m.content)[:500],
                        )

    except Exception:
        logger.exception("agent run failed")
        raise

    finally:
        elapsed = time.perf_counter() - started
        logger.info(
            "agent run finished in %.1fs | tokens in=%d out=%d",
            elapsed,
            usage["input_tokens"],
            usage["output_tokens"],
        )

    return {
        "answer": final_answer,
        "tool_calls": tool_calls,
        "usage": usage,
    }

