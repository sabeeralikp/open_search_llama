"""
FastAPI application for the search agent API.

This module provides a REST API endpoint that exposes the search agent functionality.
It configures CORS middleware to allow cross-origin requests and defines a single
endpoint for running search queries.
"""

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
    """
    Run a search query through the agent workflow.
    
    This endpoint takes a natural language query, processes it through the search
    agent workflow, and returns the generated response.
    
    Args:
        query (str): The search query to process
        
    Returns:
        dict: The workflow output containing the generated response
        
    Example:
        >>> response = await run("What is Python?")
        >>> print(response["generation"])
        "Python is a high-level programming language..."
    """
    return run_agent(query)
