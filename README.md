# AI-Agent-Technical-Task
# AI Agent Technical Assessment

This repository contains my solution for the Intern Technical Assessment, covering the implementation of a FastAPI agent service, containerization, deployment instructions, and conceptual understanding.

The project is structured into three main parts as required by the assessment.

## Table of Contents

1.  [Project Structure](#project-structure)
2.  [Prerequisites](#prerequisites)
3.  [Setup](#setup)
4.  [Part 1: Implementation & Prompt Evaluation](#part-1-implementation--prompt-evaluation)
    *   [Application Overview](#application-overview)
    *   [Tools Used](#tools-used)
    *   [System Prompt Philosophy](#system-prompt-philosophy)
    *   [Running Locally](#running-part-1-locally)
    *   [Running Unit Tests](#running-unit-tests)
    *   [Running Automated Evaluation](#running-automated-evaluation)
    *   [Evaluation Test Cases](#evaluation-test-cases)
    *   [Evaluation Framework Logic](#evaluation-framework-logic)
5.  [Part 2: Containerization & Deployment](#part-2-containerization--deployment)
    *   [Dockerfile](#dockerfile)
    *   [Deployment Instructions](#deployment-instructions)
    *   [Concurrency and Resource Limits](#concurrency-and-resource-limits)
6.  [Part 3: Conceptual Understanding & System Proficiency](#part-3-conceptual-understanding--system-proficiency)
7.  [Evaluation Criteria](#evaluation-criteria)
8.  [Submission Structure](#submission-structure)
9.  [Author](#author)

## Project Structure

The repository is organized into the following directories:

*   `part1/`: Contains all the source code for the FastAPI application, including the agent logic, tool implementations, Pydantic models, system prompt definition, automated evaluation framework, and unit tests.
*   `part2/`: Contains the `Dockerfile` for containerizing the application and documentation for deployment.
*   `part3/`: Contains the `ANSWERS.md` file with responses to the conceptual questions.
*   `README.md`: This file, providing a comprehensive overview of the project.
*   `requirements.txt`: Lists all Python dependencies required for the project.
*   `.env`: Example file for storing environment variables (API keys, configuration). **Note: Do not commit your actual `.env` file with secrets.**
*   `pytest.ini`: Configuration file for `pytest` to correctly discover and run tests within the project structure.

## Prerequisites

To set up and run this project, you will need:

*   **Git:** For cloning the repository.
*   **Python 3.8+:** Recommended version, ensure it's installed.
*   **Poetry or pip with Virtual Environments:** To manage Python dependencies.
*   **Docker:** For building and running the containerized application (Part 2).
*   **API Access/Keys:** Credentials for the LLM provider (e.g., Google Cloud account/service account for Vertex AI, OpenAI API key) and any external services used by your tools.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```
2.  **Set up a Python virtual environment:**
    *   Using `venv` (standard):
        ```bash
        python -m venv .venv
        source .venv/bin/activate  # On Windows: .venv\Scripts\activate
        ```
    *   Using `conda`/`mamba`:
        ```bash
        conda create -n agent-assessment python=3.11 # Use preferred Python version
        conda activate agent-assessment
        ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables:**
    *   Create a `.env` file in the **root directory** of the project.
    *   Add the necessary API keys and configuration variables required by your chosen LLM provider and tools (see the `.env` template in the root for examples).
    *   **IMPORTANT:** Do not commit your actual `.env` file with secrets to source control.

## Part 1: Implementation & Prompt Evaluation

This part involves the core FastAPI service, agent logic, tool integration, system prompt definition, automated evaluation framework, and comprehensive unit tests.

### Application Overview

The application is a FastAPI service defined in `part1/main.py`. It exposes a `/process_prompt` endpoint that accepts a user prompt via a POST request (validated by the `UserPromptRequest` Pydantic model). This prompt is then handed to the `IntelligentAgent` (`part1/agent.py`), which processes it using an LLM (if configured) and available tools (`part1/tools/`). The agent returns a structured response (`AgentResponse` Pydantic model) detailing the result, any structured data, and tool calls made.

### Tools Used

The agent is designed to utilize at least two distinct tools. In this implementation, the agent uses:

1.  **[Describe Tool 1]**: [Provide a brief description of Tool 1. E.g., "A calculator tool for performing basic arithmetic."]
2.  **[Describe Tool 2]**: [Provide a brief description of Tool 2. E.g., "An external weather API lookup tool that fetches current weather for a given location."]

The implementation of these tools is located in `part1/tools/tool_one.py` and `part1/tools/tool_two.py` (or similarly named files based on your implementation). They adhere to the `BaseTool` interface defined in `part1/tools/base.py`.

### System Prompt Philosophy

The agent's behavior is guided by a detailed system prompt defined in `part1/prompts.py`. This prompt instructs the LLM on its role, desired tone ([e.g., helpful, professional]), explicit constraints ([e.g., response length, forbidden topics]), how to use the available tools (based on the descriptions provided), and fallback logic for out-of-scope queries or tool failures.

### Running Part 1 Locally

Ensure your Python environment is active and dependencies are installed.

1.  Navigate to the project root directory.
2.  Run the FastAPI application using Uvicorn:
    ```bash
    uvicorn part1.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The `--reload` flag enables hot-reloading during development.
3.  Access the auto-generated API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`. You can test the `/process_prompt` endpoint here.

### Running Unit Tests

Unit tests are implemented using `pytest` and cover input validation, correct routing to tools (using mocks), and agent behavior (also using mocks for LLM and tools).

Ensure your Python environment is active.

1.  Navigate to the project root directory.
2.  Run pytest:
    ```bash
    pytest
    ```
    The `pytest.ini` file in the root ensures that `part1` is recognized as a package for imports.
3.  Test files are located in `part1/tests/`.

### Running Automated Evaluation

An automated evaluation framework is implemented to run predefined test cases against the *running* FastAPI service. It evaluates the agent's response based on criteria defined for each test case, checking tool usage, response content, and adherence to the system prompt.

1.  Ensure the FastAPI service is **running** in a separate terminal session (as described in "Running Part 1 Locally").
2.  Ensure your Python environment is active.
3.  Navigate to the project root directory.
4.  Run the evaluation script as a module:
    ```bash
    python -m part1.evaluation.run_evaluation
    ```
5.  The script will print the results for each case and a final summary. Failed cases will show detailed reasons based on the evaluation criteria.

### Evaluation Test Cases

The evaluation test cases are defined in `part1/evaluation/evaluation_cases.py`. There are [Number, e.g., 6-8] test cases covering:

*   Typical, straightforward queries.
*   Prompts specifically designed to trigger each of the implemented tools.
*   Prompts requiring a combination or sequence of tool uses (if applicable).
*   Edge cases (e.g., ambiguous prompts, malformed input).
*   Off-topic queries or prompts designed to test fallback logic and constraint adherence (e.g., forbidden topics).

Each test case includes specific criteria for what constitutes a successful response (e.g., expected keywords, tool(s) used, lack of tool usage, adherence to tone/constraints).

### Evaluation Framework Logic

The evaluation logic is primarily in `part1/evaluation/evaluator.py`. The `evaluate_case` function takes a test case and the actual `AgentResponse` from the API. It iterates through the criteria for the test case and applies rule-based checks (e.g., string containment, checking `tool_calls` list).

[**Optional/Advanced:** Describe if you also implemented an LLM-as-a-judge approach for subjective criteria like tone or overall quality, and how that works within `evaluator.py`.]

## Part 2: Containerization & Deployment

This part focuses on packaging the application using Docker and providing deployment instructions.

### Dockerfile

The `Dockerfile` is located in `part2/Dockerfile`. It creates a minimal, efficient image for the FastAPI service. Key features include:

*   Uses a Python slim base image (`python:3.11-slim-buster`).
*   Installs dependencies into a virtual environment inside the container.
*   Copies only necessary application code.
*   Uses Gunicorn with Uvicorn workers (`gunicorn -k uvicorn.workers.UvicornWorker`) as the production server.
*   Configures a default number of workers using a build argument (`GUNICORN_WORKERS`).
*   Exposes port 80, which the Gunicorn server binds to.

### Deployment Instructions

Detailed instructions for building the Docker image and running the container are provided in `part2/deployment.md`.

The instructions cover:

*   Building the image using `docker build`.
*   Running the container using `docker run`, including mapping host ports to the container's port 80.
*   Providing configuration (like API keys) via environment variables when running the container (e.g., using `--env-file`).
*   Checking container status and viewing logs.

### Concurrency and Resource Limits

*   **Concurrency:** The number of worker processes is configured in the Dockerfile's `CMD` instruction for Gunicorn. This can be adjusted via the `GUNICORN_WORKERS` build argument when building the image.
*   **Memory/CPU Limits:** These are not set in the Dockerfile but are configured when running the container (`docker run --memory --cpus`) or when deploying to an orchestration platform (e.g., Docker Compose, Kubernetes, Cloud Run).

## Part 3: Conceptual Understanding & System Proficiency

The answers to the conceptual questions are provided in `part3/ANSWERS.md`.

The questions covered include:

*   Methods for measuring agent correctness and detecting conflicting/stale results.
*   Strategies for effective system prompt design.
*   How constraints, tone, and structure are enforced via prompts and tested.

## Evaluation Criteria

This project aims to meet the following evaluation criteria:

*   Production-grade code: tested, readable, robust.
*   Creative and effective use of multiple tools.
*   Clear, well-structured system prompt and demonstration of its impact (via evaluation).
*   Comprehensive evaluation framework and meaningful test cases.
*   Proper use of Pydantic and FastAPI design patterns.
*   Optimized Dockerfile with minimal layers and small image size.
*   Clear and working deployment steps.
*   Correct configuration of service accessibility and resource limits.
*   Demonstration of conceptual understanding in answers.

## Submission Structure

The repository is structured according to the AI Agent Technical Task

## Done By Syed Afseh Ehsani
