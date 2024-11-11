"""
This module configures LLaMA language models for the search agent.

It sets up two variants of the LLaMA 3.2 model using LangChain's ChatOllama wrapper:
- A standard model for natural language generation
- A JSON-formatted model for structured output

The models are configured with temperature=0 for deterministic outputs.
"""

from langchain_community.chat_models import ChatOllama

# Defining LLM
local_llm = "llama3.2"
llama3 = ChatOllama(model=local_llm, temperature=0)
llama3_json = ChatOllama(model=local_llm, format="json", temperature=0)
