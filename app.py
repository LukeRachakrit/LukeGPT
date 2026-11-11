import os
import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="LukeGPT", page_icon="⚡")
st.title("⚡ LukeGPT")
st.caption("Custom AI Assistant built by Luke")

# Connect to Hugging Face using your secret token
client = InferenceClient(token=os.getenv("HF_TOKEN"))

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are LukeGPT, a helpful and intelligent AI assistant built by Luke."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Ask LukeGPT anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat_completion(
                    model="Qwen/Qwen2.5-7B-Instruct",
                    messages=st.session_state.messages,
                    max_tokens=250
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"Error details: {e}"
            
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
