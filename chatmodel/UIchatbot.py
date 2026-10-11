import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv(override=True)

api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Moods Of Chatbot", page_icon="🤖", layout="wide")

def get_model():
    return init_chat_model(
        "google_genai:gemini-3.6-flash",
        api_key=api_key,
        max_retries=3,
        timeout=30,
    )


if "mood" not in st.session_state:
    st.session_state.mood = None

if "msg_history" not in st.session_state:
    st.session_state.msg_history = []

if "chat_display" not in st.session_state:
    st.session_state.chat_display = []


if st.session_state.mood is None:
    st.title("🤖 Select AI Chatbot Mood")
    st.write("Choose a personality to set up your environment:")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("😡 1. Angry Mode", use_container_width=True):
            st.session_state.mood = "angry"
            st.session_state.msg_history = [SystemMessage(content="You are in an angry mood.")]
            st.rerun()

        if st.button("😂 2. Funny Mode", use_container_width=True):
            st.session_state.mood = "funny"
            st.session_state.msg_history = [SystemMessage(content="You are in a funny mood.")]
            st.rerun()

    with col2:
        if st.button("😢 3. Sad Mode", use_container_width=True):
            st.session_state.mood = "sad"
            st.session_state.msg_history = [SystemMessage(content="You are in a sad mood.")]
            st.rerun()

        if st.button("💖 4. Romantic Mode", use_container_width=True):
            st.session_state.mood = "romantic"
            st.session_state.msg_history = [SystemMessage(content="You are in a romantic mood.")]
            st.rerun()

else:
    mood = st.session_state.mood

    themes = {
        "angry": {
            "bg": "linear-gradient(135deg, #2b0000 0%, #4a0e0e 50%, #1a0000 100%)",
            "sidebar": "#1a0000",
            "chat_bg": "rgba(60, 0, 0, 0.85)",
            "border": "#ff4d4d",
            "text": "#ffffff",
            "input_bg": "#1a0000",
            "input_text": "#ffffff",
            "emoji": "🦖 🌋 🦖 🌋 🦖"
        },
        "funny": {
            "bg": "linear-gradient(135deg, #fff9c4 0%, #fff176 50%, #ffee58 100%)",
            "sidebar": "#fff59d",
            "chat_bg": "rgba(255, 255, 255, 0.95)",
            "border": "#f57f17",
            "text": "#212121",
            "input_bg": "#ffffff",
            "input_text": "#212121",
            "emoji": "😂 🤹‍♂️ 🤪 🤡 😂"
        },
        "sad": {
            "bg": "linear-gradient(135deg, #0d1b2a 0%, #1b263b 50%, #415a77 100%)",
            "sidebar": "#0b1320",
            "chat_bg": "rgba(20, 30, 48, 0.9)",
            "border": "#778da9",
            "text": "#e0e1dd",
            "input_bg": "#0b1320",
            "input_text": "#ffffff",
            "emoji": "🌧️ ☔ 💧 ☁️ 🌧️"
        },
        "romantic": {
            "bg": "linear-gradient(135deg, #ffe6e8 0%, #ffccd5 50%, #ffb3c1 100%)",
            "sidebar": "#ffb3c1",
            "chat_bg": "rgba(255, 255, 255, 0.9)",
            "border": "#ff4d6d",
            "text": "#4a0e17",
            "input_bg": "#ffffff",
            "input_text": "#4a0e17",
            "emoji": "💐 🌹 🌸 💖 🌷"
        }
    }

    t = themes[mood]

    st.markdown(f"""
        <style>
        .stApp {{
            background: {t['bg']};
            color: {t['text']} !important;
        }}
        section[data-testid="stSidebar"] {{
            background-color: {t['sidebar']} !important;
            color: {t['text']} !important;
        }}
        section[data-testid="stSidebar"] * {{
            color: {t['text']} !important;
        }}
        .stChatMessage {{
            background-color: {t['chat_bg']} !important;
            border: 1px solid {t['border']} !important;
            color: {t['text']} !important;
        }}
        /* Ensure input text fields have high contrast against backgrounds */
        [data-testid="stChatInput"] textarea {{
            background-color: {t['input_bg']} !important;
            color: {t['input_text']} !important;
        }}
        /* General text readability across all elements */
        p, span, label, div, h1, h2, h3, h4, h5, h6 {{
            color: {t['text']} !important;
        }}
        </style>
        <div style="text-align: center; font-size: 45px; padding: 10px;">{t['emoji']}</div>
    """, unsafe_allow_html=True)


    with st.sidebar:
        st.subheader(f"Current Environment: {mood.capitalize()}")
        if st.button("🔄 Switch Mood"):
            st.session_state.mood = None
            st.session_state.msg_history = []
            st.session_state.chat_display = []
            st.rerun()


    for message in st.session_state.chat_display:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    if prompt := st.chat_input("Type your message here... (or type '0' to exit)"):
        if prompt.strip() == "0":
            st.session_state.mood = None
            st.session_state.msg_history = []
            st.session_state.chat_display = []
            st.rerun()


        st.session_state.chat_display.append({"role": "user", "content": prompt})
        st.session_state.msg_history.append(HumanMessage(content=prompt))
        
        with st.chat_message("user"):
            st.markdown(prompt)


        with st.chat_message("assistant"):
            with st.spinner("Responding..."):
                try:
                    model = get_model()
                    response = model.invoke(st.session_state.msg_history)
                    
                    if isinstance(response.content, list):
                        bot_reply = response.content[0].get('text', str(response.content[0]))
                    else:
                        bot_reply = response.content

                    st.markdown(bot_reply)

                    st.session_state.msg_history.append(AIMessage(content=bot_reply))
                    st.session_state.chat_display.append({"role": "assistant", "content": bot_reply})
                except Exception as e:
                    st.error(f"Error generating response: {e}")