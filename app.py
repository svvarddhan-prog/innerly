import os
import google.generativeai as genai
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# API Key setup (Railways Variables se hi uthayega)
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

# Pura Design/UI humne Python ke andar hi store kar diya hai
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
            padding: 40px; 
            border-radius: 30px; 
            width: 320px; 
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
            height: 80px; 
            border-radius: 15px; 
            padding: 10px; 
            background: #16213e; 
            color: #fff; 
            border: 1px solid #0f3460;
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
                screen.innerHTML = `<h2>Calling Innerly...</h2><p style="font-size: 12px; color:#888;">(Voice integration loading soon)</p><br><button class="btn chat-btn" onclick="location.reload()">Back</button>`;
            } else if (mode === 'chat') {
                screen.innerHTML = `<h2>Innerly Chat</h2><textarea id="msg" placeholder="Share what's on your mind..."></textarea><br><button class="btn chat-btn" onclick="sendMsg()">Send</button><br><button class="btn call-btn" onclick="location.reload()">Back</button>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Ab Python khud hi is HTML string ko page par render karega
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    if not model:
        return jsonify({"reply": "API Key nahi mili, Railway settings check karo!"})
    user_input = request.json.get("message")
    response = model.generate_content(user_input)
    return jsonify({"reply": response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) 
