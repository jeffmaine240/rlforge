# 🧠 RL Agent FastAPI Backend

A lightweight backend project that showcases how to integrate **Reinforcement Learning (RL) agents** with **FastAPI**.  
This project dynamically supports multiple Gym environments, allowing training, evaluation, and inference through API endpoints.

---

## 🚀 Project Overview

The goal of this project is to demonstrate:
- How to wrap an **RL Agent** into a **FastAPI backend**.
- Dynamically support **different Gym environments** (e.g., `CartPole-v1`, `MountainCar-v0`).
- Expose endpoints for:
  - Creating agents with specific configs.
  - Training the agent.
  - Evaluating performance.
  - Running inference (predicting actions).

---

## 📂 Project Structure

```project/
│── app/
│ ├── api/
│ │ └── v1/
│ │ ├── routes_rl.py # API routes for RL
│ ├── core/
│ │ └── config.py # App configs
│ ├── services/
│ │ └── rl_agent_service.py # RLAgentService class
│ ├── models/
│ │ └── agent.py # RLAgent class (Gym wrapper)
│ ├── main.py # FastAPI entry point
│── requirements.txt
│── README.md

```
---

## 🔑 Key Components

### **1. RLAgent Class**
- Wraps a Gym environment.
- Handles `train()`, `evaluate()`, and `predict()` logic.
- Configurable (different envs, episodes, learning params).

### **2. RLAgentService Class**
- Manages multiple RL agents.
- Provides CRUD-like operations:
  - `create_agent()`
  - `train_agent()`
  - `evaluate_agent()`
  - `predict_action()`

### **3. FastAPI Routes**
- `POST /agents/` → create new agent.
- `POST /agents/{agent_id}/train/` → train agent.
- `POST /agents/{agent_id}/evaluate/` → evaluate.
- `POST /agents/{agent_id}/predict/` → get action for observation.

---

## ⚙️ Example Usage

### Create an Agent
```bash
POST /agents/
{
  "env_name": "CartPole-v1",
  "episodes": 100
}
```
### Train Agent
```
POST /agents/{agent_id}/train/
```

### Evaluate Agent
```
POST /agents/{agent_id}/evaluate/
```
### Predict Action
```
POST /agents/{agent_id}/predict/
{
  "observation": [0.1, -0.2, 0.05, 0.03]
}
```
## Requirements

Python 3.9+

FastAPI

Gymnasium

NumPy

Uvicorn

## Install with:
```
pip install -r requirements.txt
```
## Run the App
```
uvicorn app.main:app --reload
```

### API Docs available at:

Swagger → http://127.0.0.1:8000/docs

Redoc → http://127.0.0.1:8000/redoc