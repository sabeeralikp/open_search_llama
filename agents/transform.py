from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agents.llm import llama3_json

# Query Transformation
query_prompt = PromptTemplate(
    template="""
    
    <|begin_of_text|>
    
    <|start_header_id|>system<|end_header_id|> 
    
    You are an expert at crafting web search queries for more relevant information gain in web search.
    More often than not, a user will ask a basic question that they wish to learn more about, however it might not be in the best format. 
    Reword their query to be the most effective web search string possible.
    Return the JSON with a single key 'query' with no premable or explanation. 
    
    Question to transform: {question} 
    
    <|eot_id|>
    
    <|start_header_id|>assistant<|end_header_id|>
    
    """,
    input_variables=["question"],
)

# Chain
query_chain = query_prompt | llama3_json | JsonOutputParser()


# Node - Query Transformation
def transform_query(state):
    """
    Transform a user's natural language question into an optimized web search query.
    
    This function takes the original question from the graph state and uses an LLM to
    rewrite it into a more effective search query format. The transformation aims to
    improve search relevance by restructuring the question into keywords and phrases
    that will yield better search results.
    
    Args:
        state (dict): The current graph state containing:
            - question (str): The original user question
            
    Returns:
        dict: Updated state with new key:
            - search_query (str): The transformed search query optimized for web search
            
    Example:
        >>> state = {"question": "What did Einstein discover?"}
        >>> result = transform_query(state)
        >>> print(result["search_query"])
        "Einstein major scientific discoveries contributions physics relativity"
    """

    print("Step: Optimizing Query for Web Search")
    question = state["question"]
    gen_query = query_chain.invoke({"question": question})
    search_query = gen_query["query"]
    return {"search_query": search_query}
