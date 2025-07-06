
import pytest
from typing import Dict, Any, List, Optional


from part1.evaluation.evaluator import evaluate_case, EvaluationResult
from part1.models import AgentResponse, ToolUsage 
def create_mock_response(response_text: str, structured_data: Optional[Dict] = None, tool_calls: Optional[List[ToolUsage]] = None):
    return AgentResponse(
        response=response_text,
        structured_data=structured_data,
        tool_calls=tool_calls
    )




def test_criterion_response_contains_pass():
    case = {"case_id": "c1", "prompt": "p", "expected_outcome": {"criteria": [{"type": "response_contains", "value": "success"}]}}
    response = create_mock_response("This is a success message.")
    result = evaluate_case(case, response)
    assert result.passed is True
    assert "PASS" in str(result.details)

def test_criterion_response_contains_fail():
    case = {"case_id": "c2", "prompt": "p", "expected_outcome": {"criteria": [{"type": "response_contains", "value": "failure"}]}}
    response = create_mock_response("This response doesn't have it.")
    result = evaluate_case(case, response)
    assert result.passed is False
    assert "FAIL" in str(result.details)


def test_criterion_response_contains_keywords_pass_any():
    case = {"case_id": "c3", "prompt": "p", "expected_outcome": {"criteria": [{"type": "response_contains_keywords", "value": ["apple", "banana", "cherry"]}]}}
    response = create_mock_response("I like bananas and apples.")
    result = evaluate_case(case, response)
    assert result.passed is True
    assert "PASS" in str(result.details)

def test_criterion_response_contains_keywords_fail_any():
    case = {"case_id": "c4", "prompt": "p", "expected_outcome": {"criteria": [{"type": "response_contains_keywords", "value": ["mango", "grape"]}]}}
    response = create_mock_response("I like bananas and apples.")
    result = evaluate_case(case, response)
    assert result.passed is False
    assert "FAIL" in str(result.details)


def test_criterion_tool_used_pass():
    case = {"case_id": "c5", "prompt": "p", "expected_outcome": {"criteria": [{"type": "tool_used", "value": "MyTool"}]}}
    response = create_mock_response("Result", tool_calls=[ToolUsage(tool_name="MyTool", tool_input="", tool_output="")])
    result = evaluate_case(case, response)
    assert result.passed is True
    assert "PASS" in str(result.details)

def test_criterion_tool_used_fail():
    case = {"case_id": "c6", "prompt": "p", "expected_outcome": {"criteria": [{"type": "tool_used", "value": "MyTool"}]}}
    response_none = create_mock_response("Result", tool_calls=None)
    response_other_tool = create_mock_response("Result", tool_calls=[ToolUsage(tool_name="OtherTool", tool_input="", tool_output="")])

    result_none = evaluate_case(case, response_none)
    assert result_none.passed is False
    assert "FAIL" in str(result_none.details)

    result_other = evaluate_case(case, response_other_tool)
    assert result_other.passed is False
    assert "FAIL" in str(result_other.details)

def test_criterion_no_tool_used_pass():
    case = {"case_id": "c7", "prompt": "p", "expected_outcome": {"criteria": [{"type": "no_tool_used", "value": True}]}}
    response_none = create_mock_response("Result", tool_calls=None)
    response_empty = create_mock_response("Result", tool_calls=[])

    result_none = evaluate_case(case, response_none)
    assert result_none.passed is True
    assert "PASS" in str(result_none.details)

    result_empty = evaluate_case(case, response_empty)
    assert result_empty.passed is True
    assert "PASS" in str(result_empty.details)

def test_criterion_no_tool_used_fail():
    case = {"case_id": "c8", "prompt": "p", "expected_outcome": {"criteria": [{"type": "no_tool_used", "value": True}]}}
    response = create_mock_response("Result", tool_calls=[ToolUsage(tool_name="MyTool", tool_input="", tool_output="")])
    result = evaluate_case(case, response)
    assert result.passed is False
    assert "FAIL" in str(result.details)

def test_criterion_tool_input_contains_pass():
     case = {"case_id": "c9", "prompt": "p", "expected_outcome": {"criteria": [{"type": "tool_input_contains", "tool_name": "MyTool", "value": "specific_input"}]}}
     response = create_mock_response("Result", tool_calls=[ToolUsage(tool_name="MyTool", tool_input="some specific_input data", tool_output="")])
     result = evaluate_case(case, response)
     assert result.passed is True
     assert "PASS" in str(result.details)

def test_criterion_tool_input_contains_fail_input():
    case = {"case_id": "c10", "prompt": "p", "expected_outcome": {"criteria": [{"type": "tool_input_contains", "tool_name": "MyTool", "value": "missing_input"}]}}
    response = create_mock_response("Result", tool_calls=[ToolUsage(tool_name="MyTool", tool_input="some data", tool_output="")])
    result = evaluate_case(case, response)
    assert result.passed is False
    assert "FAIL" in str(result.details)

def test_criterion_tool_input_contains_fail_tool_not_called():
     case = {"case_id": "c11", "prompt": "p", "expected_outcome": {"criteria": [{"type": "tool_input_contains", "tool_name": "MyTool", "value": "specific_input"}]}}
     response = create_mock_response("Result", tool_calls=[ToolUsage(tool_name="OtherTool", tool_input="some specific_input data", tool_output="")]) # Input text exists, but wrong tool
     result = evaluate_case(case, response)
     assert result.passed is False
     assert "FAIL" in str(result.details)
     assert "Tool 'MyTool' was not called" in str(result.details)


def test_criterion_unknown_type():
    case = {"case_id": "c12", "prompt": "p", "expected_outcome": {"criteria": [{"type": "non_existent_criterion", "value": "anything"}]}}
    response = create_mock_response("Result")
    result = evaluate_case(case, response)
    assert result.passed is False
    assert "ERROR" in str(result.details)
    assert "Unknown or unimplemented criterion type 'non_existent_criterion'" in str(result.details)


# --- Tests for Multiple Criteria ---

def test_multiple_criteria_all_pass():
    case = {"case_id": "cm1", "prompt": "p", "expected_outcome": {"criteria": [
        {"type": "response_contains", "value": "part1"},
        {"type": "tool_used", "value": "ToolA"}
    ]}}
    response = create_mock_response("Response with part1 text.", tool_calls=[ToolUsage(tool_name="ToolA", tool_input="", tool_output="")])
    result = evaluate_case(case, response)
    assert result.passed is True
    assert "PASS" in str(result.details) # Check details for both criteria

def test_multiple_criteria_one_fail():
    case = {"case_id": "cm2", "prompt": "p", "expected_outcome": {"criteria": [
        {"type": "response_contains", "value": "part1"}, # PASS
        {"type": "tool_used", "value": "ToolB"}    # FAIL - ToolA used
    ]}}
    response = create_mock_response("Response with part1 text.", tool_calls=[ToolUsage(tool_name="ToolA", tool_input="", tool_output="")])
    result = evaluate_case(case, response)
    assert result.passed is False 
    assert "PASS" in str(result.details) 
    assert "FAIL" in str(result.details) 
