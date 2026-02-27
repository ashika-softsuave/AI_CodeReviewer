# Agentic Code Fix System

An agentic AI workflow that iteratively reviews, modifies, validates, and evaluates source code using LLM-based reasoning.

## Architecture

The system follows a multi-stage agent loop:

Review → Fix Generation → Language Detection → Validation → Evaluation → Decision

Each stage is isolated into a dedicated agent to improve reliability and control.

## Project Structure

agents/
    review_agent.py
    fix_agent.py
    validation_agent.py
    evaluation_agent.py
    decision_agent.py

services/
    agentic_service.py

utils/
    llm_client.py
    file_utils.py

config/
    ai_config.py

routes/
    agentic_routes.py

## Requirements

- Python 3.9+
- OpenAI API Key
- FastAPI

Install dependencies:

pip install -r requirements.txt

## Environment Setup

Create a `.env` file:

OPENAI_API_KEY=your_api_key_here

## Running the Server

uvicorn main:app --reload

## API Endpoint

POST /agentic-fix-file

Request Body:

{
    "instruction": "Convert this code to Python"
}

## Agent Workflow

1. Review Agent analyzes defects or mismatches
2. Fix Agent generates modified code
3. Language Detection identifies output language
4. Validation Agent checks syntax validity
5. Evaluation Agent scores solution quality
6. Decision Agent accepts or retries

## Retry Logic

The system retries up to MAX_RETRIES defined in config.

## Limitations

- Validation is LLM-based (probabilistic)
- Deterministic guarantees require compiler/runtime execution
- Language detection accuracy depends on model output quality

## Configuration

Edit config/ai_config.py:

MODEL_NAME
MAX_RETRIES
TARGET_FILE
ACCEPTANCE_THRESHOLD

## Security Notes

- Never commit `.env`
- API keys must remain local
- Avoid logging sensitive prompts/responses in production

## Running the Program

1. Prerequisites

Ensure the following are installed:

Python 3.9 or newer

pip

Internet access (required for model calls)

Check Python version:

python --version

2. Clone Repository
git clone <repository_url>
cd <project_folder>

3. Create Virtual Environment (Recommended)

Windows
python -m venv venv
venv\Scripts\activate
Linux / macOS

python -m venv venv
source venv/bin/activate

4. Install Dependencies
pip install -r requirements.txt

If no requirements.txt exists:
pip install fastapi uvicorn python-dotenv openai

5. Configure Environment Variables

Create a .env file in the project root:
OPENAI_API_KEY=your_api_key_here

Do not commit this file.

6. Verify Configuration

Edit:
config/ai_config.py
Example:

MODEL_NAME = "gpt-4o-mini"
MAX_RETRIES = 3
TARGET_FILE = "nijal.java"
ACCEPTANCE_THRESHOLD = 75


Ensure the target file exists.

7. Start the Server

uvicorn main:app --reload
Expected output:
Uvicorn running on http://127.0.0.1:8000

8. Access API Interface

Open browser:
http://127.0.0.1:8000/docs
This launches Swagger UI.

9. Execute Agent

Endpoint:
POST /agentic-fix-file
Example request body:
{
  "instruction": "Convert this code to Python"
}

10. Execution Behavior

Upon request:
Target file is loaded
Agent loop begins
Multiple model calls occur per iteration
File is overwritten only on acceptance
