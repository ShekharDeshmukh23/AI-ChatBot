import streamlit as st
import requests
import base64

# ===================== Backend API =====================
API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Secret Revelation 🤖", layout="centered")

# ===================== Encode Background Image =====================
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 👉 Change to your cyber/lock image path
bg_file = "src/assets/cyber_bg2.jpg"
bg_ext = "jpg"
bg_base64 = get_base64(bg_file)

# ===================== CSS Retro Cyber Theme =====================
st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/{bg_ext};base64,{bg_base64}") no-repeat center center fixed;
        background-size: cover;
    }}
    body {{
        color: #e0f7fa;
        font-family: "Courier New", monospace;
    }}
    .title-banner {{
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        letter-spacing: 2px;
        padding: 15px;
        margin-bottom: 15px;
        color: #00e5ff;
        text-shadow: 0 0 8px #00e5ff, 0 0 20px #ff00ff;
        animation: glitch 1.5s infinite;
    }}
    @keyframes glitch {{
        0% {{ text-shadow: 2px 0 #ff2e63, -2px 0 #45a29e; }}
        20% {{ text-shadow: -2px 0 #ff2e63, 2px 0 #45a29e; }}
        40% {{ text-shadow: 2px 0 #45a29e, -2px 0 #ff2e63; }}
        60% {{ text-shadow: -2px 0 #45a29e, 2px 0 #ff2e63; }}
        100% {{ text-shadow: 2px 0 #ff2e63, -2px 0 #45a29e; }}
    }}
    .chat-container {{
        height: 60vh;
        overflow-y: auto;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #66fcf1;
        background: rgba(0, 0, 0, 0.55);
        box-shadow: 0 0 20px #45a29e;
        margin-bottom: 15px;
    }}
    .chat-bubble {{
        padding: 12px 16px;
        margin: 10px 0;
        border-radius: 8px;
        font-size: 16px;
        max-width: 85%;
        word-wrap: break-word;
        line-height: 1.5;
    }}
    .user-bubble {{
        background: rgba(0, 229, 255, 0.1);
        color: #00e5ff;
        text-align: right;
        margin-left: auto;
        border: 1px solid #00e5ff;
        text-shadow: 0 0 5px #00e5ff;
    }}
    .bot-bubble {{
        background: rgba(255, 0, 150, 0.1);
        color: #ff80ff;
        text-align: left;
        margin-right: auto;
        border: 1px solid #ff80ff;
        text-shadow: 0 0 6px #ff00ff;
    }}
    .typing {{
        font-style: italic;
        color: #c5c6c7;
        margin-left: 10px;
        animation: blink 1s infinite;
    }}
    @keyframes blink {{ 50% {{ opacity: 0.3; }} }}
    </style>
""", unsafe_allow_html=True)

# ===================== Session State =====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===================== Title Banner =====================
st.markdown("<div class='title-banner'>⚡ Chat Bot ⚡</div>", unsafe_allow_html=True)

# Reset button
if st.button("RESET SESSION", key="reset"):
    st.session_state.messages = []
    st.rerun()

# ===================== Chat Display (Persistent Container) =====================
chat_html = "<div class='chat-container' id='chat-box'>"
for sender, msg in st.session_state.messages:
    if sender == "You":
        chat_html += f"<div class='chat-bubble user-bubble'>>> {msg}</div>"
    else:
        chat_html += f"<div class='chat-bubble bot-bubble'>{msg}</div>"
chat_html += "<div id='end'></div></div>"

chat_placeholder = st.empty()
chat_placeholder.markdown(chat_html, unsafe_allow_html=True)

# ===================== Chat Input =====================
user_input = st.chat_input(">> Type your command...")

if user_input:
    st.session_state.messages.append(("You", user_input))

    # Re-render chat immediately so user msg stays in view
    chat_html = "<div class='chat-container' id='chat-box'>"
    for sender, msg in st.session_state.messages:
        if sender == "You":
            chat_html += f"<div class='chat-bubble user-bubble'>>> {msg}</div>"
        else:
            chat_html += f"<div class='chat-bubble bot-bubble'>{msg}</div>"
    chat_html += "<div id='end'></div></div>"
    chat_placeholder.markdown(chat_html, unsafe_allow_html=True)

    # Show typing indicator (outside chat container so container doesn’t vanish)
    typing_placeholder = st.empty()
    typing_placeholder.markdown("<p class='typing'>🤖 Processing command...</p>", unsafe_allow_html=True)

    # API call
    response = requests.post(API_URL, json={"session_id": "user123", "message": user_input})
    bot_reply = response.json()["response"] if response.status_code == 200 else "⚠️ ERROR: Connection Failed"

    typing_placeholder.empty()
    st.session_state.messages.append(("Bot", bot_reply))

    # Re-render with bot reply
    chat_html = "<div class='chat-container' id='chat-box'>"
    for sender, msg in st.session_state.messages:
        if sender == "You":
            chat_html += f"<div class='chat-bubble user-bubble'>>> {msg}</div>"
        else:
            chat_html += f"<div class='chat-bubble bot-bubble'>{msg}</div>"
    chat_html += "<div id='end'></div></div>"
    chat_placeholder.markdown(chat_html, unsafe_allow_html=True)

    # Auto-scroll only inside chat box
    scroll_js = """
    <script>
        var chatBox = document.getElementById('chat-box');
        if (chatBox) {{
            chatBox.scrollTop = chatBox.scrollHeight;
        }}
    </script>
    """
    st.components.v1.html(scroll_js, height=0, width=0)
