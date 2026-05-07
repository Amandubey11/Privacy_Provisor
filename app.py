<<<<<<< HEAD
import os

# If we are in the cloud, use the cloud URL. If on your laptop, use localhost.
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/secure-chat")
import streamlit as st
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Cyber-Vault UI",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar for a cleaner look
)

# --- 2. THE "CYBER-VAULT" CSS ---
# Deep space backgrounds, glowing borders, and futuristic accents
st.markdown("""
<style>
    /* Main Background - Deep Dark Blue/Black */
    .stApp {
        background-color: #05050A;
        background-image: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #05050A 70%);
        color: #e0e0e0;
    }
    
    /* Hide default Streamlit elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Typography */
    h1, h2, h3, p {
        font-family: 'Courier New', Courier, monospace !important;
        letter-spacing: 0.5px;
    }

    /* glowing titles */
    .glow-title {
        text-align: center;
        color: #00f3ff;
        text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
        margin-top: 50px;
    }
    
    /* --- MESSAGE BUBBLES --- */
    /* Base style for all messages */
    [data-testid="stChatMessage"] {
        background-color: rgba(10, 10, 20, 0.8) !important;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 20px;
        backdrop-filter: blur(5px);
    }
    
    /* User Message (Neon Purple Glow) */
    [data-testid="stChatMessage"]:nth-child(odd) {
        border: 1px solid #b026ff;
        box-shadow: 0 0 15px rgba(176, 38, 255, 0.15);
        border-left: 4px solid #b026ff;
    }
    
    /* AI Message (Neon Cyan Glow) */
    [data-testid="stChatMessage"]:nth-child(even) {
        border: 1px solid #00f3ff;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.15);
        border-right: 4px solid #00f3ff;
    }
    
    /* --- INPUT BAR FIX --- */
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        max-width: 800px;
        z-index: 1000;
        background-color: transparent;
    }
    
    /* Input Box Glowing effect */
    .stChatInput textarea {
        background-color: rgba(5, 5, 10, 0.9) !important;
        color: #00f3ff !important;
        border: 1px solid #00f3ff !important;
        border-radius: 8px !important;
        box-shadow: 0 0 20px rgba(0, 243, 255, 0.2) !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* Input text focus */
    .stChatInput textarea:focus {
        box-shadow: 0 0 30px rgba(0, 243, 255, 0.4) !important;
        border-color: #00f3ff !important;
    }

    /* Padding for scrolling */
    .main .block-container {
        padding-bottom: 150px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LAYOUT & HEADER ---
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown("<h1 class='glow-title'>SYSTEM_LINK: ACTIVE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00f3ff;'>[ SECURE PIPELINE ESTABLISHED // PII ENCRYPTED ]</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# --- 4. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

with col2:
    for msg in st.session_state.messages:
        # Use Cyberpunk Icons
        avatar = "⚡" if msg["role"] == "user" else "💠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# --- 5. FIXED BOTTOM INPUT ---
if prompt := st.chat_input("Enter command..."):
    # Add to history and refresh immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- 6. AI PROCESSING ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with col2:
        user_prompt = st.session_state.messages[-1]["content"]
        
        with st.chat_message("assistant", avatar="💠"):
            placeholder = st.empty()
            placeholder.markdown("`Decrypting response...`")
            
            try:
                # Call Backend
                response = requests.post(BACKEND_URL, json={"prompt": user_prompt}, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    bot_reply = data["final_response_to_user"]
                    placeholder.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                else:
                    placeholder.error(f"SYS_ERR: {response.status_code}")
                    
            except Exception:
=======
import os

# If we are in the cloud, use the cloud URL. If on your laptop, use localhost.
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/secure-chat")
import streamlit as st
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Cyber-Vault UI",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar for a cleaner look
)

# --- 2. THE "CYBER-VAULT" CSS ---
# Deep space backgrounds, glowing borders, and futuristic accents
st.markdown("""
<style>
    /* Main Background - Deep Dark Blue/Black */
    .stApp {
        background-color: #05050A;
        background-image: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #05050A 70%);
        color: #e0e0e0;
    }
    
    /* Hide default Streamlit elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Typography */
    h1, h2, h3, p {
        font-family: 'Courier New', Courier, monospace !important;
        letter-spacing: 0.5px;
    }

    /* glowing titles */
    .glow-title {
        text-align: center;
        color: #00f3ff;
        text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
        margin-top: 50px;
    }
    
    /* --- MESSAGE BUBBLES --- */
    /* Base style for all messages */
    [data-testid="stChatMessage"] {
        background-color: rgba(10, 10, 20, 0.8) !important;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 20px;
        backdrop-filter: blur(5px);
    }
    
    /* User Message (Neon Purple Glow) */
    [data-testid="stChatMessage"]:nth-child(odd) {
        border: 1px solid #b026ff;
        box-shadow: 0 0 15px rgba(176, 38, 255, 0.15);
        border-left: 4px solid #b026ff;
    }
    
    /* AI Message (Neon Cyan Glow) */
    [data-testid="stChatMessage"]:nth-child(even) {
        border: 1px solid #00f3ff;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.15);
        border-right: 4px solid #00f3ff;
    }
    
    /* --- INPUT BAR FIX --- */
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        max-width: 800px;
        z-index: 1000;
        background-color: transparent;
    }
    
    /* Input Box Glowing effect */
    .stChatInput textarea {
        background-color: rgba(5, 5, 10, 0.9) !important;
        color: #00f3ff !important;
        border: 1px solid #00f3ff !important;
        border-radius: 8px !important;
        box-shadow: 0 0 20px rgba(0, 243, 255, 0.2) !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* Input text focus */
    .stChatInput textarea:focus {
        box-shadow: 0 0 30px rgba(0, 243, 255, 0.4) !important;
        border-color: #00f3ff !important;
    }

    /* Padding for scrolling */
    .main .block-container {
        padding-bottom: 150px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LAYOUT & HEADER ---
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown("<h1 class='glow-title'>SYSTEM_LINK: ACTIVE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00f3ff;'>[ SECURE PIPELINE ESTABLISHED // PII ENCRYPTED ]</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# --- 4. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

with col2:
    for msg in st.session_state.messages:
        # Use Cyberpunk Icons
        avatar = "⚡" if msg["role"] == "user" else "💠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# --- 5. FIXED BOTTOM INPUT ---
if prompt := st.chat_input("Enter command..."):
    # Add to history and refresh immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- 6. AI PROCESSING ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with col2:
        user_prompt = st.session_state.messages[-1]["content"]
        
        with st.chat_message("assistant", avatar="💠"):
            placeholder = st.empty()
            placeholder.markdown("`Decrypting response...`")
            
            try:
                # Call Backend
                response = requests.post(BACKEND_URL, json={"prompt": user_prompt}, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    bot_reply = data["final_response_to_user"]
                    placeholder.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                else:
                    placeholder.error(f"SYS_ERR: {response.status_code}")
                    
            except Exception:
>>>>>>> 9b195144be5d92762f53a2d94cb749a83a4b9079
                placeholder.error("SYS_CRITICAL: Connection to Vault Lost.")