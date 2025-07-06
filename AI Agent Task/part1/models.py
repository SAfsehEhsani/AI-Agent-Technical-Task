
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class UserPromptRequest(BaseModel):
    """
    Schema for the incoming user prompt request.
    """
    prompt: str = Field(..., description="The user's input prompt for the agent.")

class ToolUsage(BaseModel):
    """
    Schema to detail a tool call made by the agent.
    """
    tool_name: str = Field(..., description="Name of the tool used.")
    tool_input: Any = Field(..., description="Input provided to the tool.")
    tool_output: Any = Field(..., description="Output received from the tool.")
class AgentResponse(BaseModel):
    """
    Schema for the agent's structured response.
    """
    response: str = Field(..., description="The agent's final response text.")
    structured_data: Optional[Dict[str, Any]] = Field(None, description="Optional structured data derived from agent's processing.")
    tool_calls: Optional[List[ToolUsage]] = Field(None, description="Optional list detailing tool calls made by the agent during processing.")

    model_config = {
        "arbitrary_types_allowed": True
        
    }
