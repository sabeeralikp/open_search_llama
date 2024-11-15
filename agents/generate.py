"""
This module implements the generation node of the search agent workflow.

It uses a LangChain prompt template and LLM to generate natural language responses
from web search results.
"""

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.llm import llama3

# Generation Prompt
generate_prompt = PromptTemplate(
    template="""
    
    <|begin_of_text|>
    
    <|start_header_id|>system<|end_header_id|> 
    
    You are an AI assistant for Web Search, that synthesizes web search results. 
    Strictly use the following pieces of web search context to answer the question. If you don't know the answer, just say that you don't know. 
    keep the answer concise, but provide all of the details you can in the form of a report. 
    Only make direct references to material if provided in the context.
    
    <|eot_id|>
    
    <|start_header_id|>user<|end_header_id|>
    
    Question: {question} 
    Web Search Context: {context} 
    Answer: 
    
    <|eot_id|>
    
    <|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["question", "context"],
)

# Chain
generate_chain = generate_prompt | llama3 | StrOutputParser()


def generate(state):
    """
    Generate a natural language response based on web search results.
    
    This function takes the search query and web search context from the graph state,
    and uses an LLM to generate a coherent answer synthesizing the search results.
    
    Args:
        state (dict): The current graph state containing:
            - question (str): The original search query
            - context (str): Web search results and context
            
    Returns:
        dict: Updated state with new key:
            - generation (str): The LLM-generated natural language response
            
    Example:
        >>> state = {"question": "What is Python?", "context": "Python is a programming language..."}
        >>> result = generate(state)
        >>> print(result["generation"])
        "Python is a high-level programming language..."
    """
    print("Step: Generating Final Response")
    question = state["question"]
    context = state["context"]

    # Answer Generation 
    generation = generate_chain.invoke({"context": context, "question": question})
    return {"generation": generation}
