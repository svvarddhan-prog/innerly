import os
import google.generativeai as genai
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# API Key setup (Railway Variables se automatic uthayega)
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

# Pura Working Design aur JavaScript iske andar hai
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Innerly | AI Companion</title>
    <style>
        body { 
            background: #0f0f1a; 
            color: #e0e0e0; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0; 
        }
        .container { 
            background: #1a1a2e; 
            padding: 30px; 
            border-radius: 30px; 
            width: 340px; 
            text-align: center; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        h1 { color: #ff4d6d; margin-bottom: 10px; }
        .btn { 
            width: 100%; 
            padding: 15px; 
            border: none; 
            border-radius: 50px; 
            cursor: pointer; 
            font-weight: bold; 
            margin: 15px 0; 
            transition: 0.3s; 
        }
        .call-btn { background: #0f3460; border: 2px solid #ff4d6d; color: #ff4d6d; }
        .chat-btn { background: #ff4d6d; color: white; }
        textarea { 
            width: 90%; 
            height: 60px; 
            border-radius: 15px; 
            padding: 10px; 
            background: #16213e; 
            color: #fff; 
            border: 1px solid #0f3460;
            resize: none;
        }
        .chat-box {
            background: #16213e;
            padding: 15px;
            border-radius: 15px;
            max-height: 200px;
            overflow-y: auto;
            text-align: left;
            margin-bottom: 15px;
            font-size: 14px;
            line-height: 1.4;
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="appScreen">
            <h1>Innerly</h1>
            <p>Your Emotional Coach & Companion</p>
            <button class="btn call-btn" onclick="setMode('call')">📞 Voice Call Mode</button>
            <button class="btn chat-btn" onclick="setMode('chat')">💬 Chat Mode</button>
        </div>
    </div>

    <script>
        function setMode(mode) {
            const screen = document.getElementById('appScreen');
            if (mode === 'call') {
                screen.innerHTML = `
                    <h2>Calling Innerly...</h2>
                    <p style="font-size: 14px; color:#ff4d6d; font-weight:bold;">Connecting to AI Voice Server...</p>
                    <p style="font-size: 12px; color:#888;">(Bina coding ke free voice setup par hum kaam kar rahe hain)</p>
                    <br>
                    <button class="btn chat-btn" onclick="location.reload()">Disconnect</button>
                `;
            } else if (mode === 'chat') {
                screen.innerHTML = `
                    <h2>Innerly Chat</h2>
                    <div class="chat-box" id="chatBox">Innerly: Hello! Share what's on your mind...</div>
                    <textarea id="msg" placeholder="Type your message here..."></textarea>
                    <br>
                    <button class="btn chat-btn" id="sendBtn" onclick="sendMsg()">Send Message</button>
                    <button class="btn call-btn" onclick="location.reload()">Back to Menu</button>
                `;
            }
        }

        // Asli Message Sending Functionality
        async function sendMsg() {
            const msgInput = document.getElementById('msg');
            const chatBox = document.getElementById('chatBox');
            const sendBtn = document.getElementById('sendBtn');
            const message = msgInput.value.trim();

            if (!message) return;

            // Screen par user ka message dikhao
            chatBox.innerHTML += `<br><br><b>You:</b> ${message}`;
            msgInput.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            // Loading dikhao
            sendBtn.innerText = "Thinking...";
            sendBtn.disabled = true;

            try {
                // Backend Python server ko message bhejo
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                // Screen par Innerly ka reply dikhao
                chatBox.innerHTML += `<br><br><b>Innerly:</b> ${data.reply}`;
            } catch (error) {
                chatBox.innerHTML += `<br><br><span style="color:red;">Error: Server se connect nahi ho paya.</span>`;
            }

            sendBtn.innerText = "Send Message";
            sendBtn.disabled = false;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    if not model:
        return jsonify({"reply": "API Key missing! Railway settings mein GEMINI_API_KEY check karo."})
    
    try:
        user_input = request.json.get("message")
        response = model.generate_content(user_input)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
