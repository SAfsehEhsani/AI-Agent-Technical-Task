
from typing import Dict, Any, List, Optional

from part1.models import AgentResponse, ToolUsage

class EvaluationResult:
    """Represents the result of a single test case evaluation."""
    def __init__(self, case_id: str, prompt: str, passed: bool, details: Dict[str, Any]):
        self.case_id = case_id
        self.prompt = prompt
        self.passed = passed
        self.details = details 

    def __str__(self):
        status = "PASS" if self.passed else "FAIL"
        detail_str_lines = []
        for key, value in self.details.items():
             if isinstance(value, dict) and 'status' in value and 'message' in value:
                  detail_str_lines.append(f"{key}: {value['status']} - {value['message']}")
             else:
                 detail_str_lines.append(f"{key}: {value}")

        detail_str = "\n  ".join(detail_str_lines)
        return f"Case ID: {self.case_id}\nPrompt: {self.prompt}\nStatus: {status}\nDetails:\n  {detail_str}\n"


def evaluate_case(test_case: Dict[str, Any], agent_response: AgentResponse) -> EvaluationResult:
    """
    Evaluates the agent's response against the criteria defined in the test case.

    Args:
        test_case: A dictionary from evaluation_cases.py
        agent_response: The actual AgentResponse received from the API.

    Returns:
        An EvaluationResult object.
    """
    case_id = test_case.get("case_id", "unknown")
    prompt = test_case.get("prompt", "N/A")
    expected_outcome = test_case.get("expected_outcome", {})
    criteria = expected_outcome.get("criteria", [])

    evaluation_details: Dict[str, Any] = {}
    all_criteria_passed = True

    print(f"DEBUG: Evaluating case '{case_id}'...")

    
    def record_result(key, status: str, message: Any):
         nonlocal all_criteria_passed 
         evaluation_details[key] = {"status": status, "message": message}
         if status == "FAIL":
             all_criteria_passed = False

    
    for i, criterion in enumerate(criteria):
        crit_type = criterion.get("type", "unknown")
        crit_value = criterion.get("value")
        crit_key_base = f"criterion_{i+1}_{crit_type}" 

        try:
            if crit_type == "response_contains":
                expected_substring = str(crit_value)
                passed = expected_substring in agent_response.response
                record_result(crit_key_base, "PASS" if passed else "FAIL",
                              f"Response contains '{expected_substring}'")

            elif crit_type == "response_contains_keywords":
                keywords: List[str] = crit_value 
                passed = any(keyword.lower() in agent_response.response.lower() for keyword in keywords)
                 
                record_result(crit_key_base, "PASS" if passed else "FAIL",
                              f"Response contains any of keywords {keywords}")

            elif crit_type == "tool_used":
                expected_tool_name = str(crit_value)

                passed = any(tc.tool_name == expected_tool_name for tc in (agent_response.tool_calls or []))
                record_result(crit_key_base, "PASS" if passed else "FAIL",
                              f"Tool '{expected_tool_name}' was used")

            elif crit_type == "no_tool_used":
                
                passed = not agent_response.tool_calls or len(agent_response.tool_calls) == 0
                message = f"No tools used (Actual: {[tc.tool_name for tc in agent_response.tool_calls] if agent_response.tool_calls else 'None'})"
                record_result(crit_key_base, "PASS" if passed else "FAIL", message)


            elif crit_type == "tool_input_contains":
                expected_tool_name = criterion.get("tool_name")
                expected_substring = str(crit_value)
               
                matching_calls = [tc for tc in (agent_response.tool_calls or []) if tc.tool_name == expected_tool_name]

                if not matching_calls:
                    passed = False
                    message = f"Tool '{expected_tool_name}' was not called."
                else:
                    
                    tool_input_str = str(matching_calls[0].tool_input)
                    passed = expected_substring in tool_input_str
                    message = f"Input to '{expected_tool_name}' contains '{expected_substring}' (Actual input: '{tool_input_str[:100]}...') "
                record_result(crit_key_base, "PASS" if passed else "FAIL", message)

            
            else:
                passed = False
                record_result(crit_key_base, "ERROR", f"Unknown or unimplemented criterion type '{crit_type}'")


        except Exception as e:
            
            record_result(crit_key_base, "ERROR", f"Exception during evaluation: {e}")
            all_criteria_passed = False


    return EvaluationResult(
        case_id=case_id,
        prompt=prompt,
        passed=all_criteria_passed,
        details=evaluation_details
    )