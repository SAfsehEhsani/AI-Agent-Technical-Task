
import pytest

from fastapi.testclient import TestClient
import json 
from part1.main import app

from part1.models import AgentResponse, UserPromptRequest
client = TestClient(app)



def test_health_check():
    """Test the basic health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_process_prompt_valid_input():
    """Test the process_prompt endpoint with valid input."""
    prompt = "Hello, agent! What can you do?"
    response = client.post("/process_prompt", json={"prompt": prompt})

    assert response.status_code == 200
    try:
        AgentResponse.model_validate(response.json())
    except Exception as e:
        pytest.fail(f"Response did not match AgentResponse schema: {e}. Response was: {response.text}")
    
    response_data = response.json()
    assert prompt in response_data["response"]
def test_process_prompt_invalid_input_type():
    """Test the process_prompt endpoint with invalid input type."""
  
    response = client.post("/process_prompt", json={"prompt": 123})
    assert response.status_code == 422
   

def test_process_prompt_missing_field():
    """Test the process_prompt endpoint with a missing required field."""
    
    response = client.post("/process_prompt", json={})

    assert response.status_code == 422

def test_process_prompt_empty_string():
    """Test the process_prompt endpoint with an empty string."""
    
    response = client.post("/process_prompt", json={"prompt": ""})

    assert response.status_code == 400
    assert response.json()["detail"] == "Prompt must not be empty and at least 2 characters long."
