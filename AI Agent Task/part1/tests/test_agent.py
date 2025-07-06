
import pytest
from unittest.mock import AsyncMock, MagicMock 

from part1.agent import IntelligentAgent
from part1.prompts import SYSTEM_PROMPT
from part1.tools.base import BaseTool 
from part1.models import AgentResponse, ToolUsage 
def create_mock_tool(mocker, name, description, return_value, is_async=False):
    
    mock_tool = mocker.MagicMock(spec=BaseTool)
    mock_tool.name = name
    mock_tool.description = description
    if is_async:
        
         mock_tool.run = mocker.AsyncMock(return_value=return_value)
    else:
         mock_tool.run.return_value = return_value
    return mock_tool

def mock_llm_generate_content(mocker, return_text: str):
     mock_llm_response = mocker.MagicMock()
     mock_llm_response.text = return_text
    
     mock_llm_client_instance = mocker.MagicMock()
     mock_llm_client_instance.generate_content = mocker.AsyncMock(return_value=mock_llm_response) 

     mocker.patch('google.cloud.aiplatform.generative_models.GenerativeModel', return_value=mock_llm_client_instance)
@pytest.fixture
def mock_tools(mocker):
    """Fixture to provide mocked tools."""

    tool_one = create_mock_tool(mocker, "PlaceholderToolOne", "Mocks tool one.", "Mocked Result from ToolOne", is_async=False)
    tool_two = create_mock_tool(mocker, "PlaceholderToolTwo", "Mocks tool two.", "Mocked Result from ToolTwo", is_async=False)
    return [tool_one, tool_two]
@pytest.fixture
async def agent(mock_tools, mocker): 
    """Fixture to provide an Agent instance with mocked tools."""

    agent_instance = IntelligentAgent(system_prompt=SYSTEM_PROMPT, tools=mock_tools)
    
    return agent_instance
@pytest.mark.asyncio 
async def test_agent_uses_tool_one(agent, mock_tools):
    """Test that the agent attempts to use Tool One when prompted by keyword."""
    
    mock_tool_one = next(t for t in mock_tools if t.name == "PlaceholderToolOne")
    
    assert isinstance(mock_tool_one.run, MagicMock) 
    expected_tool_output = "Specific test output from ToolOne"
    mock_tool_one.run.return_value = expected_tool_output
    prompt_input = "Process this data for me using placeholder tool one: Important Data"
    response: AgentResponse = await agent.process_prompt(prompt_input)
    mock_tool_one.run.assert_called_once()
    mock_tool_one.run.assert_called_once_with("Important Data")
    assert response.tool_calls is not None
    assert len(response.tool_calls) == 1
    assert response.tool_calls[0].tool_name == "PlaceholderToolOne"
    assert response.tool_calls[0].tool_input == "Important Data" 
    assert response.tool_calls[0].tool_output == expected_tool_output
    assert expected_tool_output in response.response
    assert "Used PlaceholderToolOne" in response.response 


@pytest.mark.asyncio
async def test_agent_uses_tool_two(agent, mock_tools):
    """Test that the agent attempts to use Tool Two when prompted by keyword."""
    mock_tool_two = next(t for t in mock_tools if t.name == "PlaceholderToolTwo")
    assert isinstance(mock_tool_two.run, MagicMock) 

    expected_tool_output = "Another specific test output from ToolTwo"
    mock_tool_two.run.return_value = expected_tool_output
    prompt_input = "Please execute placeholder tool two."
    response: AgentResponse = await agent.process_prompt(prompt_input)

    mock_tool_two.run.assert_called_once()
    
    mock_tool_two.run.assert_called_once_with({"query": prompt_input}) 

    assert response.tool_calls is not None
    assert len(response.tool_calls) == 1
    assert response.tool_calls[0].tool_name == "PlaceholderToolTwo"
    assert response.tool_calls[0].tool_input == {"query": prompt_input}
    assert response.tool_calls[0].tool_output == expected_tool_output

    assert expected_tool_output in response.response
    assert "Used PlaceholderToolTwo" in response.response


@pytest.mark.asyncio
async def test_agent_uses_llm_fallback(agent, mock_tools, mocker):
    """Test that the agent falls back to LLM (simulated or actual) when no tool is triggered."""
    
    for tool in mock_tools:
        tool.run.reset_mock()

    prompt_input = "Tell me a story about a cat."
    response: AgentResponse = await agent.process_prompt(prompt_input)


    for tool in mock_tools:
        tool.run.assert_not_called()

    assert "simulated LLM response" in response.response

    assert response.tool_calls is None 


@pytest.mark.asyncio
async def test_agent_handles_tool_error(agent, mock_tools, mocker):
    """Test that the agent handles exceptions raised by tools gracefully."""
    mock_tool_one = next(t for t in mock_tools if t.name == "PlaceholderToolOne")
    assert isinstance(mock_tool_one.run, MagicMock) 

    
    error_message = "Simulated Tool Error!"
    mock_tool_one.run.side_effect = Exception(error_message) 
    


    prompt_input = "Please process data with placeholder tool one."
    response: AgentResponse = await agent.process_prompt(prompt_input)

    
    mock_tool_one.run.assert_called_once()

    assert "An error occurred while processing your request" in response.response
    assert error_message in response.response

    
    assert response.tool_calls is None 

