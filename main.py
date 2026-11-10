import os
import httpx
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# 1. Point to the free cloud endpoint for TinyLlama
API_URL = "https://huggingface.co"
HF_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# 2. Responsive dark-mode HTML template
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

history = []

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_TEMPLATE.format(chat_history="<p style='text-align:center;color:#666;'>Start a conversation above!</p>")

@app.post("/chat", response_class=HTMLResponse)
async def chat(message: str = Form(...)):
    prompt = f"<|system|>\nYou are LukeGPT, a highly intelligent and friendly AI assistant built by Luke.</s>\n<|user|>\n{message}</s>\n<|assistant|>\n"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 150, "temperature": 0.7}}
    
    # Use httpx.AsyncClient to execute a non-blocking network fetch call safely
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(API_URL, headers=headers, json=payload, timeout=60.0)
            result = response.json()
            
            # Check if Hugging Face model is still initializing on their free tier servers
            if isinstance(result, dict) and "estimated_time" in result:
                ai_response = "LukeGPT's cloud brain is warming up on Hugging Face right now. Please resend this message in 10-15 seconds!"
            else:
                raw_output = result[0]['generated_text'] if isinstance(result, list) else result['generated_text']
                ai_response = raw_output[len(prompt):].strip()
        except Exception as e:
            ai_response = "Connection timeout or model loading. Please wait a quick moment and try typing your question again!"

    # Append to visual layout block structure
    history.append(f'<div class="box user-box"><strong>You:</strong> {message}</div>')
    history.append(f'<div class="box ai-box"><strong>LukeGPT:</strong> {ai_response}</div>')
    
    chat_html = "".join(history)
    return HTML_TEMPLATE.format(chat_history=chat_html)
