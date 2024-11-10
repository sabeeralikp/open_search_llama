from typing_extensions import TypedDict


# Graph State
class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        search_query: revised question for web search
        context: web_search result
    """

    question: str
    generation: str
    search_query: str
    context: str
