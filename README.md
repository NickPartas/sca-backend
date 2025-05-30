# Spy Cat Agency - Backend

This is the backend API for the **Spy Cat Agency** assignment. It provides endpoints for managing spy cats, missions, and their assigned targets.

## 🛠 Tech Stack

- **FastAPI** – Modern web framework for building APIs
- **SQLite** – Lightweight database
- **SQLAlchemy** – ORM for Python
- **Pydantic** – Data validation and serialization
- **Uvicorn** – ASGI server

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/sca-backend.git
cd sca-backend
```

### 2. Set up virtual environment
```bash
python -m venv .venv
source .venv/bin/activate       # on Linux/macOS
.\.venv\Scripts\activate        # on Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the backend server
```bash
uvicorn app.main:app --reload --port 8000
```
## 🌐 API Documentation
```
Interactive Swagger docs will be available at:
http://localhost:8000/docs
http://localhost:8000/redoc
```
## 🔗 Postman Collection
👉 [Click here to open the Postman Collection](
https://www.postman.com/shevchenkonikita/spy-cat-agency-api/folder/gi0kbu8/spy-cat-agency-api?action=share&creator=45478550&ctx=documentation)

## 📦 API Endpoints
### 🐾 Spy Cats
| Method | Endpoint     | Description             |
| ------ | ------------ | ----------------------- |
| GET    | `/cats`      | List all spy cats       |
| GET    | `/cats/{id}` | Get a single spy cat    |
| POST   | `/cats`      | Create a new spy cat    |
| PATCH  | `/cats/{id}` | Update spy cat’s salary |
| DELETE | `/cats/{id}` | Delete a spy cat        |

✅ Breed is validated using [TheCatAPI](https://api.thecatapi.com/v1/breeds)

### 🎯 Missions & Targets
| Method | Endpoint         | Description                           |
| ------ | ---------------- | ------------------------------------- |
| GET    | `/missions`      | List all missions                     |
| GET    | `/missions/{id}` | Get a specific mission                |
| POST   | `/missions`      | Create mission with targets           |
| DELETE | `/missions/{id}` | Delete a mission (if unassigned)      |
| PATCH  | `/targets/{id}`  | Update a target (notes or completion) |
| PUT    | `/missions/{id}` | Assign a cat to a mission             |

### 📌 Notes
Uses TheCatAPI to validate cat breeds on creation.

CORS is enabled to support frontend communication (default: localhost:3000)

Errors are handled gracefully and return proper HTTP status codes.

## ✅ License
MIT © 2025 Spy Cat Agency