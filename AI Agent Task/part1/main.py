
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os

from .models import UserPromptRequest, AgentResponse
from .agent import IntelligentAgent
from .prompts import SYSTEM_PROMPT
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

app = FastAPI(
    title="Agent API",
    description="FastAPI service for an intelligent agent with tools.",
    version="1.0.0"
)
agent = IntelligentAgent(system_prompt=SYSTEM_PROMPT)


# --- Endpoint Definition ---
@app.post("/process_prompt", response_model=AgentResponse)
async def process_user_prompt(request: UserPromptRequest):
    """
    Processes a user prompt using the intelligent agent.
    """
    user_prompt = request.prompt

    
    if not user_prompt or len(user_prompt.strip()) < 2:
         raise HTTPException(status_code=400, detail="Prompt must not be empty and at least 2 characters long.")

    try:
        agent_response = await agent.process_prompt(user_prompt)
        return agent_response
    except Exception as e:
        print(f"An error occurred during agent processing: {e}", flush=True) 
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/health")
def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"}