import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="LukeGPT", page_icon="⚡")
st.title("⚡ LukeGPT")
st.caption("Custom AI Assistant built by Luke")

# Connect directly to Groq using your free API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are LukeGPT, a helpful, smart, and friendly AI assistant built by Luke."
        }
    ]

# Display past chat messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input box
if prompt := st.chat_input("Ask LukeGPT anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                   model="openai/gpt-oss-20b",
                    messages=st.session_state.messages,
                    max_tokens=500
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"Error details: {e}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
