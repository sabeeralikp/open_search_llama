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
    output = local_agent.invoke({"question": query})
    return output
