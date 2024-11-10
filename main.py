from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.base import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/run")
async def run(query: str):
    return run_agent(query)
