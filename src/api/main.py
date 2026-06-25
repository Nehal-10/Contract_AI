from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.db import (
    create_tables
)

from src.api.routes import (
    router
)

app = FastAPI(
    title="Contract AI API"
)
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

@app.on_event("startup")
def startup():

    create_tables()


@app.get("/")
def home():

    return {
        "message":
        "Contract AI Running"
    }


app.include_router(router)
