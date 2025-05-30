from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import engine
from .models import SQLModel
from .routers import cats, missions

app = FastAPI(title="Spy Cat Agency API", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SQLModel.metadata.create_all(engine)

# 👉 health-check
@app.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}

app.include_router(cats.router)
app.include_router(missions.router)
