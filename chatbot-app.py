import streamlit as st
import openai

st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
        .chatbubble {
            padding: 10px 15px;
            margin: 10px;
            border-radius: 15px;
            max-width: 70%;
            font-size: 16px;
        }
        .user {
            background-color: #dcf8c6;
            margin-left: auto;
            text-align: right;
        }
        .bot-bubble {   background-color: #f1f0f0;
            margin-right: auto;
            text-align: left;
           
        }
        .chat-container {
            border: 2px solid #ccc;
            border-radius: 10px;
            padding: 20px;
            background-color: #fafafa;
            max-width: 800px;
            margin: auto;
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Chatbot")

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "user", "content": "Hello, how can I help you today?"}]

openai.api_key = st.secrets["OPENAI_API_KEY", "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"]
model = "openai/gpt-5-chat"

with st.form("chat_form"):
    user_input = st.text_input("You:", "")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=st.session_state.messages
        )
        bot_message = response.choices[0].message['content']
    except Exception as e:
        bot_message = "Sorry, I couldn't process your request."
    st.session_state.messages.append({"role": "bot", "content": bot_message})

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chatbubble user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chatbubble bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
