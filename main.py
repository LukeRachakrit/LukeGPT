import os
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# 1. Point to the free cloud endpoint for TinyLlama
API_URL = "https://huggingface.co"
# Render will securely inject your Hugging Face API key here
HF_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# 2. The HTML code for a beautiful, responsive dark-mode chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>LukeGPT</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #e0e0e0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
        .chat-container { width: 100%; max-width: 600px; background-color: #1e1e1e; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); padding: 20px; box-sizing: border-box; }
        h1 { color: #bb86fc; text-align: center; margin-top: 0; font-size: 28px; }
        .subtitle { text-align: center; color: #a0a0a0; font-size: 14px; margin-bottom: 20px; }
        .box { padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #333; line-height: 1.5; }
        .user-box { background-color: #2c2c2c; border-left: 4px solid #03dac6; }
        .ai-box { background-color: #252525; border-left: 4px solid #bb86fc; }
        form { display: flex; gap: 10px; margin-top: 20px; }
        input[type="text"] { flex: 1; padding: 12px; border-radius: 6px; border: 1px solid #444; background-color: #2a2a2a; color: #fff; font-size: 16px; }
        input[type="text"]:focus { border-color: #bb86fc; outline: none; }
        button { padding: 12px 24px; border: none; border-radius: 6px; background-color: #bb86fc; color: #121212; font-weight: bold; font-size: 16px; cursor: pointer; transition: background 0.2s; }
        button:hover { background-color: #d7b4ff; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>⚡ LukeGPT</h1>
        <div class="subtitle">Custom Intelligent AI Assistant built by Luke</div>
        
        {chat_history}
        
        <form method="post" action="/chat">
            <input type="text" name="message" placeholder="Ask LukeGPT anything..." required autocomplete="off" autofocus>
            <button type="submit">Send</button>
        </form>
    </div>
</body>
</html>
"""

# Store current session chat history globally
history = []

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_TEMPLATE.format(chat_history="<p style='text-align:center;color:#666;'>Start a conversation above!</p>")

@app.post("/chat", response_class=HTMLResponse)
async def chat(message: str = Form(...)):
    # Format chat history context structure for the model template
    prompt = f"<|system|>\nYou are LukeGPT, a highly intelligent and friendly AI assistant built by Luke.</s>\n<|user|>\n{message}</s>\n<|assistant|>\n"
    
    # Send the lightweight payload to the Hugging Face API
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 150, "temperature": 0.7}}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    try:
        result = response.json()
        raw_output = result['generated_text']
        # Isolate the newly generated response text cleanly
        ai_response = raw_output[len(prompt):].strip()
    except Exception:
        ai_response = "LukeGPT is waking up or processing. Please try submitting your message again in a few seconds!"

    # Append new conversation turn to history display blocks
    history.append(f'<div class="box user-box"><strong>You:</strong> {message}</div>')
    history.append(f'<div class="box ai-box"><strong>LukeGPT:</strong> {ai_response}</div>')
    
    chat_html = "".join(history)
    return HTML_TEMPLATE.format(chat_history=chat_html)
