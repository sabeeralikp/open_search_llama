from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# Web Search Tool
wrapper = DuckDuckGoSearchAPIWrapper(max_results=25)
web_search_tool = DuckDuckGoSearchRun(api_wrapper=wrapper)


# Node - Web Search
def web_search(state):
    """
    Perform web search using DuckDuckGo based on the search query.
    
    This function takes a transformed search query from the graph state and uses
    DuckDuckGo's search API to retrieve relevant web results. It handles API errors
    by retrying failed requests.
    
    Args:
        state (dict): The current graph state containing:
            - search_query (str): The transformed search query to use
            
    Returns:
        dict: Updated state with new key:
            - context (str): The raw search results from DuckDuckGo
            
    Example:
        >>> state = {"search_query": "Python programming language"}
        >>> result = web_search(state)
        >>> print(result["context"])
        "Python is a high-level programming language..."
    """

    search_query = state["search_query"]
    print(f'Step: Searching the Web for: "{search_query}"')

    # Web search tool call
    while True:
        try:
            search_result = web_search_tool.invoke(search_query)
            return {"context": search_result}
        except Exception as e:
            print(e)
            continue
