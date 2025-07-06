
from typing import List
import httpx 
import os
from dotenv import load_dotenv
import time
import asyncio
from part1.evaluation.evaluation_cases import get_evaluation_cases
from part1.evaluation.evaluator import evaluate_case, EvaluationResult
from part1.models import AgentResponse 
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path)

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
PROCESS_ENDPOINT = f"{API_BASE_URL}/process_prompt"
REQUEST_DELAY_SECONDS = 0.5 
API_TIMEOUT_SECONDS = 120


async def run_all_evaluations():
    """Runs all defined evaluation test cases against the deployed API."""
    test_cases = get_evaluation_cases()
    results: List[EvaluationResult] = []
    async with httpx.AsyncClient() as client:

        print(f"Starting automated evaluation against {API_BASE_URL}...")
        print(f"Found {len(test_cases)} test cases.")

        for i, case in enumerate(test_cases):
            case_id = case.get("case_id", f"case_{i+1}")
            prompt = case["prompt"]
            print(f"\n--- Running Case {i+1}/{len(test_cases)}: {case_id} ---")
            print(f"Prompt: {prompt}")

            agent_response = None
            api_call_status = "FAIL"
            api_call_details = "No API call made due to error setup."

            try:
                
                print(f"Calling POST {PROCESS_ENDPOINT} with prompt: '{prompt[:50]}...'")
                response = await client.post(
                    PROCESS_ENDPOINT,
                    json={"prompt": prompt},
                    timeout=API_TIMEOUT_SECONDS
                )
                response.raise_for_status() 
                agent_response = AgentResponse.model_validate(response.json())
                api_call_status = "PASS"
                api_call_details = "Successfully received and parsed response."
                print(f"API Call Status: PASS (HTTP {response.status_code})")
                print(f"Received response (first 150 chars): {agent_response.response[:150]}...")
                if agent_response.tool_calls:
                    print(f"  Tool calls detected: {[tc.tool_name for tc in agent_response.tool_calls]}")
                else:
                     print("  No tool calls detected.")


            except httpx.HTTPStatusError as e:
                api_call_details = f"HTTP Error: {e.response.status_code} - {e.response.text}"
                print(f"API Call Status: FAIL ({api_call_details})")
            except httpx.RequestError as e:
                api_call_details = f"Request Error: {e}"
                print(f"API Call Status: FAIL ({api_call_details})")
            except Exception as e:
                api_call_details = f"Unexpected Error during API call: {e}"
                print(f"API Call Status: FAIL ({api_call_details})")
            evaluation_details_for_case = {
                "API Call Status": {"status": api_call_status, "message": api_call_details}
            }
            if agent_response:
                evaluation_result = evaluate_case(case, agent_response)
                evaluation_details_for_case.update(evaluation_result.details)
                final_case_passed = evaluation_result.passed and (api_call_status == "PASS")
            else:
                final_case_passed = False


            final_result = EvaluationResult(
                 case_id=case_id,
                 prompt=prompt,
                 passed=final_case_passed,
                 details=evaluation_details_for_case 
            )
            results.append(final_result)

            print(f"Case {case_id} OVERALL status: {'PASS' if final_result.passed else 'FAIL'}")

            await asyncio.sleep(REQUEST_DELAY_SECONDS)


        print("\n--- Evaluation Summary ---")
        total_cases = len(results)
        passed_cases = sum(1 for r in results if r.passed)
        failed_cases = total_cases - passed_cases

        print(f"Total Cases: {total_cases}")
        print(f"Passed: {passed_cases}")
        print(f"Failed: {failed_cases}")

        if failed_cases > 0:
            print("\nFailed Cases Details:")
            for result in results:
                if not result.passed:
                    print(result)
        return failed_cases == 0 
if __name__ == "__main__":
    print("--- Automated Evaluation Runner ---")
    print(f"Attempting to connect to API at: {PROCESS_ENDPOINT}")
    print("Ensure your FastAPI service is running in a separate terminal.")
    print("Example: navigate to the project root and run `uvicorn part1.main:app --reload`")
    print("-" * 30)

    try:
        asyncio.run(run_all_evaluations())
    except Exception as e:
        print(f"\nAn error occurred while running the evaluation script: {e}")
        print("Please ensure the FastAPI service is running and accessible at the specified URL.")