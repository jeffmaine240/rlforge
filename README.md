# 🧠 RL Agent FastAPI Backend

A lightweight backend project that integrates **Reinforcement Learning (RL) agents** with **FastAPI**.  
This project allows you to register, train, and interact with custom RL agents through a clean and extensible API.

---

## 🚀 Features
- **Environment Management**
  - Create, configure, and update Gym-like environments.
  - Save and restore agent states.
- **Agent Training**
  - Trigger training sessions and monitor progress.
  - Store training metadata such as rewards, episode counts, and timestamps.
- **Database Integration**
  - PostgreSQL with SQLAlchemy + Alembic for migrations.
  - Async database operations for scalability.
- **Logging & Debugging**
  - Structured logs for session commits and training runs.

---

## 📂 Project Structure
```bash
project/
│── app/
│   ├── api/           # API routes (v1, environments, agents, etc.)
│   ├── core/          # Core settings & config
│   ├── db/            # Database session & models
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic (training, inference, etc.)
│   ├── utils/         # Helpers (datetime, logging, etc.)
│   └── main.py        # FastAPI entrypoint
│
│── alembic/           # Database migrations
│── tests/             # Unit & integration tests
│── README.md
│── requirements.txt 
```

---


# ⚙️ Installation

## 1. Clone the repository
```bash
git clone <your-repo-url>
cd project
```
## 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate
```
## 3. Install dependencies
```bash
pip install -r requirements/base.txt
```
## 4. Set up environment variables

Create a .env file:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/rl_backend
```
## 5. Run migrations
```bash
alembic upgrade head
```
## 6. Start the server
```bash
uvicorn app.main:app --reload
```
## 📡 API Endpoints

### 🌍 Environments
- **POST** `/api/v1/environments` → Create a new environment  
- **POST** `/api/v1/environments/{name}/step` → Perform a step in the environment  
- **POST** `/api/v1/environments/{name}/reset` → Reset an environment  
- **DELETE** `/api/v1/environments/{name}` → Delete an environment  

---

### 🔐 Authentication
- **POST** `/api/v1/auth/register` → Register  
- **POST** `/api/v1/auth/login` → Login  
- **POST** `/api/v1/auth/refresh-access-token` → Refresh Access Token  
- **POST** `/api/v1/auth/logout` → Logout  

---

### 🏋️ Training
- **POST** `/api/v1/training/{env_name}/start` → Start Training  
- **POST** `/api/v1/training/{env_name}/stop` → Stop Training  
- **GET** `/api/v1/training/{env_name}/status` → Training Status  
- **GET** `/api/v1/training/{env_name}/history` → Training History  



## 🛠️ Tech Stack

Backend: FastAPI, Pydantic
Database: PostgreSQL, SQLAlchemy (async), Alembic
ML: Custom RL agent logic (Gym-compatible)
Others: Uvicorn, Asyncpg, Python 3.10+


✅ Status

✅ Environment registration & state saving
✅ Training session logic with database persistence
✅ user authentication for RBAC
⏳ Advanced monitoring (coming soon)
⏳ Frontend dashboard (planned)