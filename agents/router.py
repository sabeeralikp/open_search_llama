"""
This module implements the routing logic for the search agent workflow.

It uses a LangChain prompt template and LLM to determine whether a user question
should be routed to web search or directly to response generation. The routing
decision is based on whether additional context would improve the answer quality.

The module provides:
- A prompt template for routing decisions
- A chain combining the prompt with a JSON-outputting LLM
- A routing function that executes the chain and returns the next node
"""

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agents.llm import llama3_json

# Router
router_prompt = PromptTemplate(
    template="""
    
    <|begin_of_text|>
    
    <|start_header_id|>system<|end_header_id|>
    
    You are an expert at routing a user question to either the generation stage or web search. 
    Use the web search for questions that require more context for a better answer, or recent events.
    Otherwise, you can skip and go straight to the generation phase to respond.
    You do not need to be stringent with the keywords in the question related to these topics.
    Give a binary choice 'web_search' or 'generate' based on the question. 
    Return the JSON with a single key 'choice' with no premable or explanation. 
    
    Question to route: {question} 
    
    <|eot_id|>
    
    <|start_header_id|>assistant<|end_header_id|>
    
    """,
    input_variables=["question"],
)

# Chain
question_router = router_prompt | llama3_json | JsonOutputParser()


# Conditional Edge, Routing
def route_question(state):
    """
    Route a user question to either web search or direct generation.
    
    This function analyzes the question to determine whether additional context from
    web search would improve the answer quality. Questions about recent events or
    requiring specific factual details are routed to web search, while general
    knowledge questions go directly to generation.
    
    Args:
        state (dict): The current graph state containing:
            - question (str): The user's original question
            
    Returns:
        str: The next node to call in the workflow graph:
            - "websearch": Route to web search for additional context
            - "generate": Route directly to response generation
            
    Example:
        >>> state = {"question": "What happened in the news today?"}
        >>> route_question(state)
        'websearch'
    """

    print("Step: Routing Query")
    question = state["question"]
    output = question_router.invoke({"question": question})
    if output["choice"] == "web_search":
        print("Step: Routing Query to Web Search")
        return "websearch"
    elif output["choice"] == "generate":
        print("Step: Routing Query to Generation")
        return "generate"
