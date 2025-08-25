import streamlit as st
import requests
import base64

# ===================== Backend API =====================
API_URL = "http://127.0.0.1:8000/chat"
st.set_page_config(page_title="Secret Revelation 🤖", layout="wide")

# ===================== Session State =====================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "bot_personality" not in st.session_state:
    st.session_state.bot_personality = "Mysterious Guide"

# ===================== Encode Background Image =====================
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_file = "src/assets/cyber_bg2.jpg"
bg_ext = "jpg"
bg_base64 = get_base64(bg_file)

# ===================== CSS Cyber Theme =====================
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
  font-size: 38px;
  font-weight: bold;
  letter-spacing: 2px;
  padding: 10px;
  margin-bottom: 8px;
  color: #00e5ff;
  text-shadow: 0 0 8px #00e5ff, 0 0 20px #ff00ff;
  animation: glitch 1.5s infinite;
}}
@keyframes glitch {{
  0%   {{ text-shadow: 2px 0 #ff2e63, -2px 0 #45a29e; }}
  20%  {{ text-shadow: -2px 0 #ff2e63, 2px 0 #45a29e; }}
  40%  {{ text-shadow: 2px 0 #45a29e, -2px 0 #ff2e63; }}
  60%  {{ text-shadow: -2px 0 #45a29e, 2px 0 #ff2e63; }}
  100% {{ text-shadow: 2px 0 #ff2e63, -2px 0 #45a29e; }}
}}
.chat-container {{
  height: 60vh; 
  width: 86%;
  overflow-y: auto;
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #66fcf1;
  background: rgba(0, 0, 0, 0.55);
  box-shadow: 0 0 20px #45a29e;
  margin: 0 auto 15px auto;
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
  background: rgba(0, 229, 255, 0.12);
  color: #00e5ff;
  text-align: right;
  margin-left: auto;
  border: 1px solid #00e5ff;
  text-shadow: 0 0 5px #00e5ff;
}}
.bot-bubble {{
  background: rgba(255, 0, 150, 0.12);
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

# ===================== Title =====================
ironman_icon = "src/assets/ironman.png"  # path to your Iron Man mask icon

st.markdown(f"""
<div class='title-banner'>
    <img src="data:image/png;base64,{get_base64(ironman_icon)}" 
         style="height:65px;vertical-align:middle;margin-right:15px;">
    Chat Bot
    <img src="data:image/png;base64,{get_base64(ironman_icon)}" 
         style="height:65px;vertical-align:middle;margin-left:15px;">
</div>
""", unsafe_allow_html=True)


# ===================== Sidebar =====================
with st.sidebar:
    st.subheader("🧭 Navigation")
    if st.button("➕ New Chat"):
        st.session_state.chat_history.append(st.session_state.messages)
        st.session_state.messages = []
        st.rerun()

    st.write("📜 **Chat History**")
    if st.session_state.chat_history:
        for i, hist in enumerate(st.session_state.chat_history):
            st.markdown(f"- Chat {i+1} ({len(hist)} msgs)")

    st.divider()
    st.subheader("⚙️ Settings")

    st.session_state.bot_personality = st.radio(
        "Bot Personality",
        ["Mysterious Guide", "Tony Stark", "Zen Monk", "Funny Joker"],
        index=["Mysterious Guide", "Tony Stark", "Zen Monk", "Funny Joker"].index(st.session_state.bot_personality)
    )

    if st.checkbox("🔑 Show Secret Hint"):
        st.info("Solve 2 riddles correctly to unlock the hidden key!")

    st.write("📊 **Session Stats**")
    st.write(f"Messages exchanged: {len(st.session_state.messages)}")

# ===================== Chat Display =====================
chat_html = "<div class='chat-container' id='chat-box'>"
for sender, msg in st.session_state.messages:
    if sender == "You":
        chat_html += f"<div class='chat-bubble user-bubble'>>> {msg}</div>"
    else:
        chat_html += f"<div class='chat-bubble bot-bubble'>{msg}</div>"
chat_html += "<div id='end'></div></div>"

chat_placeholder = st.empty()
chat_placeholder.markdown(chat_html, unsafe_allow_html=True)

# ===================== Input + API =====================
user_input = st.chat_input(">> Type your command...")

if user_input:
    st.session_state.messages.append(("You", user_input))

    # Re-render with user message
    chat_html = "<div class='chat-container' id='chat-box'>"
    for sender, msg in st.session_state.messages:
        chat_html += (
            f"<div class='chat-bubble user-bubble'>>> {msg}</div>"
            if sender == "You" else
            f"<div class='chat-bubble bot-bubble'>{msg}</div>"
        )
    chat_html += "<div id='end'></div></div>"
    chat_placeholder.markdown(chat_html, unsafe_allow_html=True)

    typing_placeholder = st.empty()
    typing_placeholder.markdown("<p class='typing'>🤖 Processing command...</p>", unsafe_allow_html=True)

    response = requests.post(API_URL, json={
        "session_id": "user123",
        "message": f"[{st.session_state.bot_personality}] {user_input}"
    })
    bot_reply = response.json()["response"] if response.status_code == 200 else "⚠️ ERROR: Connection Failed"
    typing_placeholder.empty()

    st.session_state.messages.append(("Bot", bot_reply))

    # Re-render with bot reply
    chat_html = "<div class='chat-container' id='chat-box'>"
    for sender, msg in st.session_state.messages:
        chat_html += (
            f"<div class='chat-bubble user-bubble'>>> {msg}</div>"
            if sender == "You" else
            f"<div class='chat-bubble bot-bubble'>{msg}</div>"
        )
    chat_html += "<div id='end'></div></div>"
    chat_placeholder.markdown(chat_html, unsafe_allow_html=True)

    # Auto-scroll inside chat container
    st.components.v1.html("""
        <script>
            var chatBox = document.getElementById('chat-box');
            if (chatBox) { chatBox.scrollTop = chatBox.scrollHeight; }
        </script>
    """, height=0, width=0)
