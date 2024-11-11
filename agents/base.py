"""
This module implements a search agent workflow using LangGraph.

The workflow consists of multiple nodes for web search, query transformation,
and response generation, connected in a directed graph.

Author: Sabeerali
Created: 10 Nov 2024
"""

from langgraph.graph import END, StateGraph

from agents.graph import GraphState
from agents.search import web_search
from agents.transform import transform_query
from agents.generate import generate
from agents.router import route_question

# Build the nodes
workflow = StateGraph(GraphState)
workflow.add_node("websearch", web_search)
workflow.add_node("transform_query", transform_query)
workflow.add_node("generate", generate)

# Build the edges
workflow.set_conditional_entry_point(
    route_question,
    {
        "websearch": "transform_query",
        "generate": "generate",
    },
)
workflow.add_edge("transform_query", "websearch")
workflow.add_edge("websearch", "generate")
workflow.add_edge("generate", END)

# Compile the workflow
local_agent = workflow.compile()


def run_agent(query):
    """
    Execute the search agent workflow with the given query.

    Args:
        query (str): The search query to process

    Returns:
        dict: The output from the workflow execution

    """
    output = local_agent.invoke({"question": query})
    return output
