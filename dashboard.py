import streamlit as st
import requests

# Title and Layout
st.set_page_config(page_title="LLM Privacy Vault", layout="wide")
st.title("🛡️ LLM Privacy Vault")
st.markdown("### Zero-Trust Proxy for GenAI")

# Sidebar for settings
with st.sidebar:
    st.header("System Status")
    st.success("Vault Active")
    st.info("Backend: http://127.0.0.1:8000")

# Input Area
user_input = st.text_area("Enter your prompt (try including an email or phone number):", height=100)
send_btn = st.button("🔒 Anonymize & Send")

# Columns for Split View
col1, col2 = st.columns(2)

if send_btn and user_input:
    # 1. Call your FastAPI Backend
    try:
        response = requests.post(
            "http://127.0.0.1:8000/secure-chat",
            json={"prompt": user_input}
        )
        data = response.json()

        # 2. Show Results
        with col1:
            st.subheader("👤 User Perspective")
            st.markdown("**Input:**")
            st.info(user_input)
            st.markdown("**Final Response:**")
            st.success(data["final_response_to_user"])

        with col2:
            st.subheader("🤖 AI/Server Perspective")
            st.markdown("**What the AI Received:**")
            st.warning(data["sanitized_sent_to_llm"])
            st.markdown("**Raw AI Response:**")
            st.code(data["raw_llm_response"])

    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        st.caption("Make sure 'main.py' is running in a separate terminal!")