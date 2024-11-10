from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# Web Search Tool
wrapper = DuckDuckGoSearchAPIWrapper(max_results=25)
web_search_tool = DuckDuckGoSearchRun(api_wrapper=wrapper)


# Node - Web Search
def web_search(state):
    """
    Web search based on the question

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended web results to context
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
