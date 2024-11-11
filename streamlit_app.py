"""
Streamlit web interface for the Open Search Llama agent.

This module provides a chat-based interface for interacting with the search agent API.
It maintains chat history across sessions and displays messages in a conversational format.

The interface allows users to:
- Configure the base URL for the search agent API
- Send search queries through a chat input
- View conversation history with the agent
"""

from requests import get
import streamlit as st

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.title("Open Search Llama")

BASE_URL = st.text_input("Base URL")


def run_request(query: str) -> str:
    """
    Send a search query to the agent API and return the response.

    Makes a GET request to the configured API endpoint with the user's query
    and returns the generated response if successful.

    Args:
        query (str): The search query to send to the agent

    Returns:
        str: The generated response from the agent
        
    Note:
        Prints response text to console on error
    """
    response = get(f"{BASE_URL}/run", params={"query": query})
    if response.status_code == 200:
        return response.json()["generation"]
    print(response.text)


# React to user input
if prompt := st.chat_input("Surf with search agent"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = run_request(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
