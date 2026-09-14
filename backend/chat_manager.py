import streamlit as st
import uuid
from datetime import datetime

from utils.storage import (
    save_chat,
    load_chat,
    load_all_chats,
    delete_chat,
    rename_chat
)


def get_user_id():
    return st.session_state.user["id"]


def initialize_chat():

    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = str(
            uuid.uuid4()
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []


def create_new_chat():
    st.session_state.current_chat_id = str(
        uuid.uuid4()
    )
    st.session_state.messages = []

    if "document_text" in st.session_state:
        del st.session_state["document_text"]

    if "document_name" in st.session_state:
        del st.session_state["document_name"]


def add_message(role, content):

    st.session_state.messages.append(
        {
            "role": role,
            "content": content
        }
    )


def save_current_chat():

    messages = st.session_state.messages

    if not messages:
        return

    first_user_message = next(
        (
            message["content"]
            for message in messages
            if message["role"] == "user"
        ),
        "New Chat"
    )

    title = first_user_message[:40]

    chat_data = {
        "id": st.session_state.current_chat_id,
        "title": title,
        "messages": messages,
        "updated_at": datetime.now().isoformat()
    }

    save_chat(
        get_user_id(),
        st.session_state.current_chat_id,
        chat_data
    )


def get_chat_history():

    return load_all_chats(
        get_user_id()
    )


def load_existing_chat(chat_id):

    chat = load_chat(
        get_user_id(),
        chat_id
    )

    if chat:

        st.session_state.current_chat_id = chat_id

        st.session_state.messages = chat["messages"]


def remove_chat(chat_id):

    delete_chat(
        get_user_id(),
        chat_id
    )

    if (
        st.session_state.current_chat_id
        == chat_id
    ):
        create_new_chat()


def rename_existing_chat(
    chat_id,
    new_title
):

    rename_chat(
        get_user_id(),
        chat_id,
        new_title
    )