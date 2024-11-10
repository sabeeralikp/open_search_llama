from langchain_community.chat_models import ChatOllama

# Defining LLM
local_llm = "llama3.2"
llama3 = ChatOllama(model=local_llm, temperature=0)
llama3_json = ChatOllama(model=local_llm, format="json", temperature=0)
