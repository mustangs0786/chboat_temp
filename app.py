import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini Chatbot")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
st.text(AIzaSyAUlQXOs4PTe_whSs9FwoDh6K0qOBTRpSY)
# Sidebar for API key input
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="Enter your Gemini API key")
    model_choice = st.selectbox("Model", ["gemini-flash-latest", "gemini-pro-latest"], index=0)
    thinking_level = st.selectbox("Thinking Level", ["HIGH", "MEDIUM", "LOW"], index=0)
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
        st.stop()

    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build contents from full chat history
    contents = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg["content"])],
            )
        )

    # Stream response from Gemini
    try:
        client = genai.Client(api_key=api_key)
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level=thinking_level),
        )

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            for chunk in client.models.generate_content_stream(
                model=model_choice,
                contents=contents,
                config=config,
            ):
                if chunk.text:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(f"Error: {e}")
