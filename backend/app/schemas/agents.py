from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ToolCallInfo(BaseModel):
    name: str
    args: dict


class Usage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0


class AgentResponse(BaseModel):
    answer: str
    tool_calls: list[ToolCallInfo]
    usage: Usage