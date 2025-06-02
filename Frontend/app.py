import streamlit as st
import requests
import json
import pandas as pd

BACKEND_API_URL = "http://127.0.0.1:8005/chat"
CLEAR_CHAT_URL = "http://127.0.0.1:8005/clear_chat"

def get_chatbot_response(user_query):
    try:
        payload = {"message": user_query, "conversation_id": "1"}
        response = requests.post(BACKEND_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        return {"error": f"API request failed: {e}"}
    except json.JSONDecodeError:
        return {"error": "Failed to decode JSON response from API."}

# --- MAIN APP ---
def main():
    st.set_page_config(page_title="Data Analyst Chatbot", page_icon="🤖")

    st.markdown("<h2 style='text-align: center;'>🤖 AskLytics</h2><br><h3 style='text-align: center;'>Data Analyst Chatbot</h3>", unsafe_allow_html=True)

    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history using st.chat_message
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

    # Input at the bottom (inside st.chat_input)
    user_input = st.chat_input("Ask your data question here:")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Processing your query..."):
            response = get_chatbot_response(user_input)

        st.session_state.chat_history.append({"role": "bot", "content": response})
        with st.chat_message("bot"):
            try:
                df = pd.DataFrame(response["output"])
                st.dataframe(df, use_container_width=True)
            except:
                st.error("Invalid response format.")

    # Clear chat button
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        try:
            response = requests.post(CLEAR_CHAT_URL, json={"conversation_id": "1"})
            response.raise_for_status()
            st.success("Chat history cleared successfully.")
        except requests.RequestException as e:
            st.error(f"Failed to clear chat history: {e}")
        st.rerun()

if __name__ == "__main__":
    main()
