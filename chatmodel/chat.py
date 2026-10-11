# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv(override=True)

# from langchain.chat_models import init_chat_model
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# model = init_chat_model(
#     "google_genai:gemini-3.6-flash",
#     max_retries=10,  # Increase for unreliable networks (default: 6)
#     timeout=120,  # Seconds; increase for slow connections
# )

# print("what mood do you wish your model to possess?")
# print("press 1 for angry mode")
# print("press 2 for funny mode")
# print("press 3 for sad mode")
# print("press 4 for romantic mode")

# n = input("press the number")

# mood = ""

# if n == "1":
#    mood = "You are in an angry mood"
# elif n == "2":
#      mood = "You are in an funny mood"
# elif n == "3":
#      mood = "You are in an sad mood"
# elif n == "4":
#      mood = "You are in an romantic mood"          

# msg_history = [
#     SystemMessage(content = mood )
# ]

# print("press 0 to exit the conversation")

# while True:

#     prompt = input("enter your query : ")
#     if prompt == "0":
#        break;         
    
#     msg_history.append( HumanMessage(content=prompt) ) 
      
#     response = model.invoke(msg_history)
#     msg_history.append( AIMessage(content=response.content[0]['text'] ) )
#     print(response.content[0]['text'])


import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Set page config for a clean and responsive layout
st.set_page_config(
    page_title="Dynamic Mood AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for different mood themes and styling
st.markdown("""
<style>
    .main {
        background-color: var(--background-color);
        transition: background-color 0.5s ease;
    }
    .mood-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

if "mood" not in st.session_state:
    st.session_state.mood = None
if "mood_name" not in st.session_state:
    st.session_state.mood_name = None
if "msg_history" not in st.session_state:
    st.session_state.msg_history = []

# Function to reset conversation and mood
def reset_mood():
    st.session_state.mood = None
    st.session_state.mood_name = None
    st.session_state.msg_history = []
    st.rerun()

if st.session_state.mood is None:
    st.markdown("<h1 class='mood-title'>🌟 Welcome to the Mood AI Chatbot 🌟</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center; color: gray; font-size: 1.1rem;'>Choose a mood for your AI companion below to begin the experience.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 1. Angry Mode")
        st.write("Fierce, short-tempered responses with dinosaur energy!")
        if st.button("Select Angry Mode", key="btn_angry"):
            st.session_state.mood = "You are in an angry mood"
            st.session_state.mood_name = "Angry"
            st.session_state.msg_history = [SystemMessage(content=st.session_state.mood)]
            st.rerun()
            
        st.markdown("### 😢 3. Sad Mode")
        st.write("Melancholic, gloomy, with gentle raining vibes.")
        if st.button("Select Sad Mode", key="btn_sad"):
            st.session_state.mood = "You are in an sad mood"
            st.session_state.mood_name = "Sad"
            st.session_state.msg_history = [SystemMessage(content=st.session_state.mood)]
            st.rerun()

    with col2:
        st.markdown("### 😂 2. Funny Mode")
        st.write("Jokes, laughing scenes, and humorous banter.")
        if st.button("Select Funny Mode", key="btn_funny"):
            st.session_state.mood = "You are in an funny mood"
            st.session_state.mood_name = "Funny"
            st.session_state.msg_history = [SystemMessage(content=st.session_state.mood)]
            st.rerun()
            
        st.markdown("### 💖 4. Romantic Mode")
        st.write("Affectionate, poetic, surrounded by flowers and roses.")
        if st.button("Select Romantic Mode", key="btn_romantic"):
            st.session_state.mood = "You are in an romantic mood"
            st.session_state.mood_name = "Romantic"
            st.session_state.msg_history = [SystemMessage(content=st.session_state.mood)]
            st.rerun()

else:
    mood_name = st.session_state.mood_name
    
    # Render dynamic theme headers, decorations, and animations
    if mood_name == "Angry":
        st.markdown("<h2 style='text-align: center; color: #ff4d4d;'>🦖 Angry Mode Active: ROAR! Watch out! 🦖</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>🌋 *The ground shakes with dinosaur footsteps...*</p>", unsafe_allow_html=True)
    elif mood_name == "Funny":
        st.markdown("<h2 style='text-align: center; color: #ffcc00;'>😂 Funny Mode Active: Keep on Laughing! 🎭</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>🎉 *Canned laughter and cheerful chuckles fill the air...*</p>", unsafe_allow_html=True)
    elif mood_name == "Sad":
        st.markdown("<h2 style='text-align: center; color: #4da6ff;'>🌧️ Sad Mode Active: Gentle Rain Falling... ☔</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>💧 *Pitter-patter of raindrops against the window...*</p>", unsafe_allow_html=True)
    elif mood_name == "Romantic":
        st.markdown("<h2 style='text-align: center; color: #ff66b2;'>🌹 Romantic Mode Active: Blooming Flowers & Poetry 💐</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>🌸 *Sweet fragrances and rose petals floating around...*</p>", unsafe_allow_html=True)

    st.sidebar.markdown(f"### Current Mood: **{mood_name}**")
    if st.sidebar.button("🔄 Change Mood / Reset"):
        reset_mood()
    if st.sidebar.button("🚪 Exit / Clear Chat"):
        reset_mood()

    st.markdown("---")

    # Initialize the model matching your provided specification
    try:
        model = init_chat_model(
            "google_genai:gemini-3.6-flash",
            max_retries=10,
            timeout=120,
        )
    except Exception:
        # Fallback initializer if needed
        model = init_chat_model(
            "google_genai:gemini-2.5-flash",
            max_retries=10,
            timeout=120,
        )

    # Display message history (skipping the system message at index 0 for UI clarity)
    for message in st.session_state.msg_history[1:]:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)

    # Chat input box replicating the terminal input loop
    if prompt := st.chat_input("Enter your query (or type '0' to exit):"):
        if prompt.strip() == "0":
            reset_mood()
        
        # Append human message to history
        st.session_state.msg_history.append(HumanMessage(content=prompt))
        
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Thinking in character..."):
                try:
                    response = model.invoke(st.session_state.msg_history)
                    # Safely handle response content structure
                    if hasattr(response, 'content'):
                        if isinstance(response.content, list) and len(response.content) > 0 and 'text' in response.content[0]:
                            reply_text = response.content[0]['text']
                        else:
                            reply_text = str(response.content)
                    else:
                        reply_text = str(response)
                        
                    st.markdown(reply_text)
                    st.session_state.msg_history.append(AIMessage(content=reply_text))
                except Exception as e:
                    error_msg = f"An error occurred while invoking the model: {e}"
                    st.error(error_msg)
                    st.session_state.msg_history.append(AIMessage(content=error_msg))