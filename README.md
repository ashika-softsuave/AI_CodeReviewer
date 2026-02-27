# AI Code Reviewer with Supervised Fix–Retry Agentic Loop

## 🚀 Overview

This project implements a multi-agent AI system that autonomously reviews, fixes, validates, evaluates, and iteratively improves source code until it meets a predefined quality threshold.

Unlike traditional one-shot AI code reviewers, this system uses a supervised agentic loop with dynamic orchestration, convergence detection, rewrite safety, and cost tracking.

---

## 🧠 Core Concept

The system follows this intelligent workflow:

1. Review the code
2. Generate fixes
3. Validate syntax
4. Evaluate quality
5. Detect stagnation (plateau)
6. Retry or accept based on Supervisor decision

A Supervisor Agent dynamically controls which agents run during each iteration.

---

## 🏗️ Architecture

API Layer (FastAPI)  
        ↓  
Service Layer (Orchestrator)  
        ↓  
Supervisor Agent (Planner)  
        ↓  
Worker Agents:  
- Review Agent  
- Fix Agent  
- Validation Agent  
- Evaluation Agent  
- Diff Agent  
        ↓  
OpenAI Model  

---

## ⚙️ Key Features

- Iterative Fix → Evaluate → Retry loop
- Dynamic agent selection via Supervisor
- Syntax validation gating
- Rewrite safety using diff analysis
- Plateau detection (convergence control)
- Maximum retry protection
- Token usage tracking (cost awareness)
- Persistent iteration memory
- REST API interface using FastAPI

---

## 📂 Project Structure

AI_CodeReviewer/

- main.py  
- routes/route.py  
- services/agentic_service.py  
- agents/  
  - review_agent.py  
  - fix_agent.py  
  - evaluation_agent.py  
  - validation_agent.py  
  - decision_agent.py  
  - supervisor_agent.py  
  - diff_agent.py  
  - memory_agent.py  
- utils/  
  - llm_client.py  
  - file_utils.py  
- config/ai_config.py  
- agent_memory.json  
- requirements.txt  
- .env  

---

## 🔁 Workflow Explanation

### Step 1 – User Request

User sends instruction:

{
  "instruction": "Fix bugs in the file"
}

---

### Step 2 – Orchestration Begins

- Target file is loaded
- System state initialized
- Supervisor created
- Iterative loop begins

---

### Step 3 – Supervisor Planning

Supervisor evaluates:

- Current retry count
- Quality score
- Validation failure status
- Rewrite percentage
- Plateau condition

It decides:

- Stop
- Accept
- Continue
- Which agents to execute

---

### Step 4 – Dynamic Agent Execution

Depending on the plan, selected agents run:

- Review → Identify issues  
- Fix → Generate improved code  
- Validate → Check syntax correctness  
- Evaluate → Score quality improvement  
- Diff → Measure rewrite percentage  

---

### Step 5 – Convergence Control

Loop stops when:

- Score ≥ acceptance threshold  
- Plateau detected  
- Maximum retries reached  

System guarantees termination.

---

## 🤖 Model Usage

Configured in `config/ai_config.py`.

Used for:

- Code review reasoning
- Fix generation
- Syntax validation
- Quality evaluation
- Language detection

Temperature is set to 0 for deterministic behavior.

---

## 📊 Safety & Control Mechanisms

| Mechanism | Purpose |
|------------|----------|
| Validation Gating | Prevents evaluation of broken code |
| Diff Analysis | Prevents full file rewrites |
| Plateau Detection | Stops useless retries |
| Max Retry Limit | Guarantees loop termination |
| Token Tracking | Monitors API usage cost |

---

## 🔧 Installation

### 1. Clone Repository

git clone https://github.com/yourusername/AI_CodeReviewer.git  
cd AI_CodeReviewer  

### 2. Create Virtual Environment

python -m venv .venv  

Activate:

Windows:
.venv\Scripts\activate  

Mac/Linux:
source .venv/bin/activate  

### 3. Install Dependencies

pip install -r requirements.txt  

### 4. Create .env File

Create a `.env` file in root directory:

OPENAI_API_KEY=your_api_key_here  

---

## ▶️ Run Application

uvicorn main:app --reload  

Open:

http://127.0.0.1:8000/docs  

Use Swagger UI to test the API.

---

## 📈 Example API Response

{
  "status": "success",
  "score": 82,
  "retries": 2,
  "tokens": {
    "iteration1": 950,
    "iteration2": 820
  },
  "total_tokens": 1770
}

---



