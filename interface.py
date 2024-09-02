
import streamlit as st

from chatgpt import llm_chat
from history import History


def create_interface():
    emoji = "❤️"
    st.set_page_config(
        page_title=f"Casanova GPT",
        page_icon=emoji,
        layout="wide"
    )

    st.title(f"Casanova GPT")

    # check for messages in session and create if not exists
    if "history" not in st.session_state.keys():
        st.session_state.history = History()
        st.session_state.history.system(f"You are a dating coach on tinder and you help anyone that wants to increase "
                                        f"their chances of dating the person is looking for, and making sure their are "
                                        f"equiped with the right information to make sure that becomes a reality.")
        st.session_state.history.assistant("Hello there, how can I help you? " + emoji + "\n")

    # Display all messages
    for message in st.session_state.history.logs:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_prompt = st.chat_input()

    if user_prompt is not None:
        st.session_state.history.user(user_prompt)
        with st.chat_message("user"):
            st.write(user_prompt)

    if st.session_state.history.logs[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Loading..."):
                chat = llm_chat(st.session_state.history)
                st.write(chat)
        st.session_state.history.assistant(chat)
