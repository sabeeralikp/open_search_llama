from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.base import llama3

# Generation Prompt
generate_prompt = PromptTemplate(
    template="""
    
    <|begin_of_text|>
    
    <|start_header_id|>system<|end_header_id|> 
    
    You are an AI assistant for Web Search, that synthesizes web search results. 
    Strictly use the following pieces of web search context to answer the question. If you don't know the answer, just say that you don't know. 
    keep the answer concise, but provide all of the details you can in the form of a report, Cite the sources also. 
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


# Node - Generate
def generate(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """

    print("Step: Generating Final Response")
    question = state["question"]
    context = state["context"]

    # Answer Generation
    generation = generate_chain.invoke({"context": context, "question": question})
    return {"generation": generation}
