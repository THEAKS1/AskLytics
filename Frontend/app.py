import streamlit as st
import requests
import json
import pandas as pd

BACKEND_API_URL = "http://127.0.0.1:8005/chat"
CLEAR_CHAT_URL = "http://127.0.0.1:8005/clear_chat"

def get_chatbot_response(user_input, conversation_id):
    payload = {"message": user_input, "conversation_id": conversation_id}
    try:
        response = requests.post(BACKEND_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        data = {"error": f"API Error: {e}"}

# --- MAIN APP ---
def main():
    st.set_page_config(page_title="Data Analyst Chatbot", page_icon="🤖")

    # Step 1: Ask for user's email address
    if "email" not in st.session_state:
        st.session_state.email = None

    if not st.session_state.email:
        st.markdown("<h2 style='text-align: center;'>🤖 AskLytics</h2>", unsafe_allow_html=True)
        st.markdown("### Please enter your email address to start:")
        email_input = st.text_input("Email Address", placeholder="you@example.com")

        if st.button("Start Chat"):
            if email_input and "@" in email_input:
                st.session_state.email = email_input.strip()
                st.success("Email saved. You can now start chatting!")
                st.rerun()
            else:
                st.error("Please enter a valid email address.")
        return

    # Step 2: Normal Chatbot Page
    st.markdown("<h2 style='text-align: center;'>🤖 AskLytics</h2><br><h3 style='text-align: center;'>Data Analyst Chatbot</h3>", unsafe_allow_html=True)

    # Back button to switch account
    if st.button("🔙 Back to Login / Switch Account"):
        st.session_state.email = None
        st.session_state.chat_history = []
        st.rerun()
        
    # Initialize session state for chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            if msg["role"] == "bot":
                try:
                    df = pd.DataFrame(msg["content"]["output"])
                    st.dataframe(df, use_container_width=True)
                except:
                    st.error("Invalid response format.")
            else:
                st.markdown(msg["content"])

    # User query input
    user_input = st.chat_input("Ask your data question here:")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Processing your query..."):
            data = get_chatbot_response(user_input, st.session_state.email)

        st.session_state.chat_history.append({"role": "bot", "content": data})
        with st.chat_message("bot"):
            try:
                df = pd.DataFrame(data["output"])
                st.dataframe(df, use_container_width=True)
            except:
                st.error("Invalid response format.")

    # Clear chat button
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        try:
            response = requests.post(CLEAR_CHAT_URL, json={"conversation_id": st.session_state.email})
            response.raise_for_status()
            st.success("Chat history cleared successfully.")
        except requests.RequestException as e:
            st.error(f"Failed to clear chat history: {e}")
        st.rerun()


if __name__ == "__main__":
    main()
