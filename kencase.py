import os
import json
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.core.messages import HumanMessage, SystemMessage, AIMessage

# Page Configuration
st.set_page_config(page_title="AI Agent Interface", page_icon="🤖", layout="wide")
st.title("🤖 Personal AI Agent")

# Sidebar Configuration
st.sidebar.header("Agent Settings")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.0, 0.2, 0.1)

# System Prompt Configuration
system_prompt = st.sidebar.text_area(
    "System Instructions",
    value="You are a helpful, smart, and precise AI assistant. Answer user queries accurately and clearly.",
    height=150
)

# Initialize Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI agent. How can I assist you today?"}
    ]

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input Logic
if user_input := st.chat_input("Type your message here..."):
    if not openai_api_key:
        st.error("Please enter your OpenAI API Key in the sidebar to start chatting.")
        st.stop()

    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Format messages for LangChain
    formatted_messages = [SystemMessage(content=system_prompt)]
    for m in st.session_state.messages:
        if m["role"] == "user":
            formatted_messages.append(HumanMessage(content=m["content"]))
        elif m["role"] == "assistant":
            formatted_messages.append(AIMessage(content=m["content"]))

    # Call OpenAI Model
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key, temperature=temperature)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(formatted_messages)
            st.write(response.content)
            
    st.session_state.messages.append({"role": "assistant", "content": response.content})