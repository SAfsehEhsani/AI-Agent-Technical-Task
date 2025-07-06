
from typing import List, Dict, Any, Optional

from part1.models import AgentResponse, ToolUsage
from part1.prompts import SYSTEM_PROMPT
from part1.tools import AVAILABLE_TOOLS, TOOL_MAP 


class IntelligentAgent:
    """
    The core agent responsible for processing prompts, using tools,
    and generating responses based on the system prompt.
    """
    def __init__(self, system_prompt: str = SYSTEM_PROMPT, tools: List[Any] = AVAILABLE_TOOLS):
        self.system_prompt = system_prompt
        self.tools = tools
        self.tool_map = {tool.name: tool for tool in self.tools} 
        print("WARNING: LLM client not initialized. Using simulated responses.")
        self.llm = None 

    async def process_prompt(self, user_prompt: str) -> AgentResponse:
        """
        Processes the user's prompt. This involves reasoning, tool use,
        and response generation guided by the system prompt.
        """
        print(f"Agent processing prompt: {user_prompt}") 


        called_tools_info: List[ToolUsage] = []
        final_response_text = ""
        structured_output_data: Optional[Dict[str, Any]] = None
        try:
            if "tool one" in user_prompt.lower() or "placeholder tool one" in user_prompt.lower():
                tool_name_to_call = "PlaceholderToolOne" 
                tool_instance = self.tool_map.get(tool_name_to_call)
                if tool_instance:
                    
                    tool_input = user_prompt.replace("tool one", "").replace("placeholder tool one", "").strip()
                    print(f"DEBUG: Agent deciding to use {tool_name_to_call} with input '{tool_input}'")
                    
                    tool_output = tool_instance.run(tool_input)
                    called_tools_info.append(ToolUsage(
                        tool_name=tool_name_to_call,
                        tool_input=tool_input,
                        tool_output=tool_output
                    ))
                    final_response_text = f"Used {tool_name_to_call}. Result: {tool_output}. Based on this: [Synthesize final response here, possibly using LLM]"
                    
                else:
                    final_response_text = f"Tried to use {tool_name_to_call} but it wasn't found or initialized."
                    print(f"ERROR: Tool '{tool_name_to_call}' not found in TOOL_MAP.")


            elif "tool two" in user_prompt.lower() or "placeholder tool two" in user_prompt.lower():
                tool_name_to_call = "PlaceholderToolTwo" # Use the actual name
                tool_instance = self.tool_map.get(tool_name_to_call)
                if tool_instance:
                    
                    tool_input = {"query": user_prompt} # Example input structure
                    print(f"DEBUG: Agent deciding to use {tool_name_to_call} with input '{tool_input}'")
                    
                    tool_output = tool_instance.run(tool_input)
                    called_tools_info.append(ToolUsage(
                        tool_name=tool_name_to_call,
                        tool_input=tool_input,
                        tool_output=tool_output
                    ))
                    final_response_text = f"Used {tool_name_to_call}. Result: {tool_output}. Based on this: [Synthesize final response here, possibly using LLM]"
                else:
                    final_response_text = f"Tried to use {tool_name_to_call} but it wasn't found or initialized."
                    print(f"ERROR: Tool '{tool_name_to_call}' not found in TOOL_MAP.")

            else:
                
                print("DEBUG: No specific tool triggered by keywords. Falling back to simulated LLM response.")
                if self.llm:
                    
                     final_response_text = f"Agent (simulated LLM): Based on your request '{user_prompt}', I can provide information. [Add a generic, helpful response here]."


                else:
                    
                    final_response_text = f"Agent: I received your prompt: '{user_prompt}'. My advanced functions (LLM) are not currently available, and no specific tools were triggered by keywords."


        except Exception as e:
            
            print(f"ERROR in agent processing chain: {e}")
            final_response_text = f"Agent: An error occurred while processing your request: {e}. Please try again."
            
        return AgentResponse(
            response=final_response_text,
            structured_data=structured_output_data, 
            tool_calls=called_tools_info if called_tools_info else None 
        )