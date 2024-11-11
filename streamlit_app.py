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

# Page config
st.set_page_config(page_title="Open Search Llama", page_icon="🦙", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        # box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #f0f2f6;
    }
    .assistant-message {
        background-color: #e8f0fe;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar configuration
with st.sidebar:
    st.title("Open Search Llama")
    st.markdown("---")
    BASE_URL = st.text_input("API Base URL", placeholder="http://localhost:8000")
    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "Your Personal, Private Search Assistant powered by LangChain and Llama 3.2"
    )

# Main chat interface
st.header("🦙 Chat with Open Search Llama")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(
            f'<div class="chat-message {message["role"]}-message">{message["content"]}</div>',
            unsafe_allow_html=True,
        )


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
    if not BASE_URL:
        st.error("⚠️ Please enter a base URL in the sidebar")
        return

    with st.spinner("🔍 Searching for answers..."):
        response = get(f"{BASE_URL}/run", params={"query": query})
        if response.status_code == 200:
            return response.json()["generation"]
        st.error(f"❌ Error: {response.text}")


# Chat input
if prompt := st.chat_input("Ask me anything...", key="chat_input"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(
            f'<div class="chat-message user-message">{prompt}</div>',
            unsafe_allow_html=True,
        )
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get and display assistant response
    response = run_request(prompt)
    if response:
        with st.chat_message("assistant"):
            st.markdown(
                f'<div class="chat-message assistant-message">{response}</div>',
                unsafe_allow_html=True,
            )
        st.session_state.messages.append({"role": "assistant", "content": response})
