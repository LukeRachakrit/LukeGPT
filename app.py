import os
import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="LukeGPT", page_icon="⚡")
st.title("⚡ LukeGPT")
st.caption("Custom AI Assistant built by Luke")

# Connect to Hugging Face using your secret token
client = InferenceClient(token=os.getenv("HF_TOKEN"))

# Set up chat memory so the webpage displays your conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are LukeGPT, a helpful and intelligent AI assistant built by Luke."}
    ]

# Show past messages on screen
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input box at the bottom
if prompt := st.chat_input("Ask LukeGPT anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat_completion(
                    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                    messages=st.session_state.messages,
                    max_tokens=200
                )
                reply = response.choices[0].message.content
            except Exception:
                reply = "LukeGPT is waking up on the cloud server. Please try sending your message again in 10 seconds!"
            
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
