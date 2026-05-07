import gradio as gr
import requests

# --- 1. CONFIGURATION & THEME COLORS ---
# We define the specific colors from the Dribbble design (Dark + Neon Green)
THEME_COLOR = "#00dc82"  # Vibrant Green
BACKGROUND_DARK = "#0f1117" # Deep Dark Blue/Black
COMPONENT_BG = "#1e293b" # Slightly lighter for cards

# --- 2. THE CUSTOM CSS (The "Design" Logic) ---
custom_css = f"""
/* Hide the standard Gradio footer */
footer {{visibility: hidden !important;}}

/* Main Background */
body, .gradio-container {{
    background-color: {BACKGROUND_DARK} !important;
    color: white !important;
}}

/* The Chatbot Window */
#chatbot {{
    height: 70vh !important; 
    background-color: {BACKGROUND_DARK} !important;
    border: 1px solid #334155;
    border-radius: 15px;
}}

/* User Message Bubble (Green) */
.user-message {{
    background-color: {THEME_COLOR} !important;
    color: #000 !important; /* Black text on green */
    border-radius: 15px 15px 0 15px !important; /* Unique shape */
    font-weight: 500;
}}

/* AI Message Bubble (Dark Grey) */
.bot-message {{
    background-color: {COMPONENT_BG} !important;
    color: #e2e8f0 !important; /* White/Grey text */
    border-radius: 15px 15px 15px 0 !important;
    border: 1px solid #334155;
}}

/* Input Bar Styling */
textarea {{
    background-color: {COMPONENT_BG} !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}}

/* The 'Send' Button */
#send-btn {{
    background-color: {THEME_COLOR} !important;
    color: black !important;
    font-weight: bold;
    border: none;
    border-radius: 8px;
}}
"""

# --- 3. CHAT LOGIC ---
def chat_logic(message, history):
    if not message:
        return "", history

    # Update history immediately with user message
    history = history + [[message, None]]
    
    try:
        # Call your local backend (main.py)
        response = requests.post(
            "http://127.0.0.1:8000/secure-chat",
            json={"prompt": message},
            timeout=45
        )
        
        if response.status_code == 200:
            data = response.json()
            bot_reply = data["final_response_to_user"]
        else:
            bot_reply = f"❌ Server Error: {response.status_code}"
            
    except Exception as e:
        bot_reply = "⚠️ Error: Is 'main.py' running?"

    # Update history with bot reply
    history[-1][1] = bot_reply
    return "", history

# --- 4. BUILDING THE UI (Layout) ---
with gr.Blocks(theme=gr.themes.Base(), css=custom_css, title="Secure AI Vault") as demo:
    
    with gr.Row():
        # --- LEFT SIDEBAR ---
        with gr.Column(scale=1, min_width=250, visible=True):
            gr.Markdown(f"## 🛡️ Privacy Vault")
            gr.Markdown("Your data is encrypted and anonymized before touching the AI.")
            
            # Fake "History" buttons to look like the design
            gr.Button("📁 Project Mars", variant="secondary")
            gr.Button("📁 Tesla Emails", variant="secondary")
            gr.Button("➕ New Chat", variant="primary")
            
            with gr.Accordion("⚙️ Settings", open=False):
                gr.Checkbox(label="Anonymize Emails", value=True)
                gr.Checkbox(label="Anonymize Phones", value=True)
                gr.Slider(label="Security Level", minimum=1, maximum=5, value=5)

        # --- MAIN CHAT AREA ---
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(
                label="Secure Workspace",
                elem_id="chatbot",
                bubble_full_width=False,
                avatar_images=(None, "https://cdn-icons-png.flaticon.com/512/4712/4712027.png") 
            )
            
            with gr.Row():
                msg_input = gr.Textbox(
                    show_label=False,
                    placeholder="Type your secure message...",
                    scale=4,
                    container=False
                )
                send_btn = gr.Button("➤", elem_id="send-btn", scale=0)

    # --- 5. EVENT LISTENERS ---
    # Allow pressing "Enter" or clicking the button
    msg_input.submit(chat_logic, [msg_input, chatbot], [msg_input, chatbot])
    send_btn.click(chat_logic, [msg_input, chatbot], [msg_input, chatbot])

# --- 6. LAUNCH ---
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)