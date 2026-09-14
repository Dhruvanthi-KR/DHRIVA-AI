import streamlit as st
from pypdf import PdfReader
from utils.auth import init_auth_db

from backend.groq_client import get_response_stream
from backend.chat_manager import (
    initialize_chat,
    create_new_chat,
    add_message,
    save_current_chat,
    get_chat_history,
    load_existing_chat,
    remove_chat,
    rename_existing_chat
)

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="DHRIVA",
    page_icon="assets/bot-message-square.svg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_auth_db()

# ==================================================
# AUTHENTICATION
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ==================================================
# LOAD CSS
# ==================================================

with open("frontend/style.css", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==================================================
# LOGIN / SIGN UP
# ==================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <div class="auth-container">
            <div class="auth-title">✦ DHRIVA</div>
            <div class="auth-subtitle">AI Assistant</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:

        if st.session_state.get("signup_success", False):
            st.success(
                "Account created successfully! Please log in."
            )
            st.session_state.signup_success = False

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            from utils.auth import authenticate_user

            user = authenticate_user(
                email,
                password
            )

            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()

            else:
                st.error(
                    "Invalid email or password."
                )

    with signup_tab:

        new_email = st.text_input(
            "Email",
            key="signup_email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not new_email or not new_password:

                st.error(
                    "Please enter your email and password."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(new_password) < 6:

                st.error(
                    "Password must be at least 6 characters."
                )

            else:

                from utils.auth import create_user

                created = create_user(
                    new_email,
                    new_password
                )

                if created:

                    st.success(
                        "Account created successfully! You can now log in with your new account."
                    )

                else:

                    st.error(
                        "An account with this email already exists."
                    )

    st.stop()

# ==================================================
# INITIALIZE CHAT
# ==================================================

initialize_chat()

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("✦ DHRIVA")
    st.caption("AI Assistant")

    st.divider()

    # New Chat

    if st.button(
        "＋  New Chat",
        use_container_width=True
    ):

        create_new_chat()
        st.rerun()

    st.divider()

    # Chat History

    st.markdown("##### RECENT CHATS")

    chats = get_chat_history()

    search_chat = st.text_input(
        "Search chats",
        placeholder="🔍 Search chats...",
        label_visibility="collapsed"
    )

    chats = get_chat_history()

    if search_chat.strip():

        chats = [
            chat
            for chat in chats
            if search_chat.lower() in chat["title"].lower()
        ]

    if chats:

        for chat in chats:

            chat_id = chat["id"]
            title = chat["title"]

            col1, col2 = st.columns(
                [5, 1],
                gap="small"
            )

            # Open Chat

            with col1:

                if st.button(
                    f"💬 {title}",
                    key=f"chat_{chat_id}",
                    use_container_width=True
                ):

                    load_existing_chat(chat_id)
                    st.rerun()

            # Three Dot Menu

            with col2:

                if st.button(
                    "⋯",
                    key=f"menu_{chat_id}",
                    use_container_width=True
                ):

                    st.session_state[
                        f"show_menu_{chat_id}"
                    ] = not st.session_state.get(
                        f"show_menu_{chat_id}",
                        False
                    )

            # Rename / Delete

            if st.session_state.get(
                f"show_menu_{chat_id}",
                False
            ):

                new_title = st.text_input(
                    "Chat name",
                    value=title,
                    key=f"rename_{chat_id}"
                )

                if st.button(
                    "Rename",
                    key=f"rename_button_{chat_id}",
                    use_container_width=True
                ):

                    if new_title.strip():

                        rename_existing_chat(
                            chat_id,
                            new_title.strip()
                        )

                        st.session_state[
                            f"show_menu_{chat_id}"
                        ] = False

                        st.rerun()

                if st.button(
                    "Delete",
                    key=f"delete_{chat_id}",
                    use_container_width=True
                ):

                    remove_chat(chat_id)

                    st.session_state[
                        f"show_menu_{chat_id}"
                    ] = False

                    st.rerun()

    else:

        st.caption("No previous chats yet.")

    # EXPORT CHAT

    if st.session_state.messages:

        st.markdown("##### EXPORT CHAT")

        txt_content = ""

        for message in st.session_state.messages:

            role = message["role"].upper()

            txt_content += f"{role}:\n"
            txt_content += message["content"]
            txt_content += "\n\n"

        st.download_button(
            "⬇ Download TXT",
            data=txt_content,
            file_name="dhriva_chat.txt",
            mime="text/plain",
            use_container_width=True
        )

        import json

        json_content = json.dumps(
            st.session_state.messages,
            indent=4,
            ensure_ascii=False
        )

        st.download_button(
            "⬇ Download JSON",
            data=json_content,
            file_name="dhriva_chat.json",
            mime="application/json",
            use_container_width=True
        )

    st.divider()

    # USER ACCOUNT

    st.markdown(
        f"""
        <div class="user-account">
            <div class="user-icon">👤</div>
            <div class="user-email">
                {st.session_state.user["email"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🚪  Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.messages = []

        if "current_chat_id" in st.session_state:
            del st.session_state["current_chat_id"]

        st.rerun()

    st.caption("✦ Powered by Groq")


# ==================================================
# WELCOME SCREEN
# ==================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        """<div class="welcome-screen">
<div class="welcome-icon">✦</div>
<div class="welcome-title">How can I help you today?</div>
<div class="welcome-subtitle">Ask anything, or upload a PDF to get started.</div>
</div>""",
        unsafe_allow_html=True
    )

# ==================================================
# DISPLAY CHAT HISTORY
# ==================================================

for index, message in enumerate(
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        # Regenerate Assistant Response

        if message["role"] == "assistant":

            if st.button(
                "↻ Regenerate",
                key=f"regenerate_{index}"
            ):

                st.session_state.messages.pop(
                    index
                )

                try:

                    ai_messages = st.session_state.messages.copy()

                    if st.session_state.get("document_text"):

                        ai_messages.insert(
                            0,
                            {
                                "role": "system",
                                "content": (
                                    "The user has uploaded a document. "
                                    "Answer questions about the document using ONLY "
                                    "the document content below. "
                                    "If the answer is not present in the document, "
                                    "say that it is not available in the document.\n\n"
                                    "DOCUMENT:\n"
                                    + st.session_state.document_text
                                )
                            }
                        )

                    response = st.write_stream(
                        get_response_stream(
                            ai_messages
                        )
                    )

                    add_message(
                        "assistant",
                        response
                    )

                    save_current_chat()

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )

# ==================================================
# CHAT INPUT + PDF UPLOAD
# ==================================================

prompt_data = st.chat_input(
    "Message DHRIVA...",
    accept_file="multiple",
    file_type=["pdf"],
    max_upload_size=200
)

prompt = ""

if prompt_data:

    prompt = prompt_data.text.strip()

    uploaded_files = prompt_data.files

    # Process uploaded PDFs

    if uploaded_files:

        document_text = ""
        document_names = []

        for uploaded_file in uploaded_files:

            try:

                reader = PdfReader(uploaded_file)

                pdf_text = ""

                for page in reader.pages:

                    text = page.extract_text()

                    if text:
                        pdf_text += text + "\n"

                # OCR FALLBACK FOR SCANNED PDFs

                if not pdf_text.strip():

                    from pdf2image import convert_from_bytes
                    import pytesseract

                    pdf_bytes = uploaded_file.getvalue()

                    images = convert_from_bytes(
                        pdf_bytes
                    )

                    for image in images:

                        text = pytesseract.image_to_string(
                            image
                        )

                        if text:
                            pdf_text += text + "\n"

                if pdf_text.strip():

                    document_text += (
                        f"\n\n===== {uploaded_file.name} =====\n\n"
                        + pdf_text
                    )

                    document_names.append(
                        uploaded_file.name
                    )

                else:

                    st.warning(
                        f"Could not extract text from {uploaded_file.name}."
                    )

            except Exception:

                st.error(
                    f"Unable to read {uploaded_file.name}. "
                    "Please try another PDF."
                )

        if document_text.strip():

            st.session_state.document_text = document_text

            st.session_state.document_name = ", ".join(
                document_names
            )

            st.success(
                f"{len(document_names)} PDF(s) uploaded successfully."
            )

    # Validate message

    if not prompt and uploaded_files:

        prompt = (
            "Please analyze the uploaded document"
            if len(uploaded_files) == 1
            else "Please analyze the uploaded documents"
        )

    if prompt:

        if len(prompt) > 5000:

            st.warning(
                "Your message is too long. Please keep it under 5000 characters."
            )

            st.stop()

# ==================================================
# HANDLE USER MESSAGE
# ==================================================

if prompt:

    # Save user message

    add_message(
        "user",
        prompt
    )

    # Show user message

    with st.chat_message("user"):

        st.markdown(prompt)

    # Generate assistant response

    try:

        with st.chat_message("assistant"):

            ai_messages = st.session_state.messages.copy()

            if st.session_state.get("document_text"):

                ai_messages.insert(
                    0,
                    {
                        "role": "system",
                        "content": (
                            "The user has uploaded a document. "
                            "Answer questions about the document using ONLY "
                            "the document content below. "
                            "If the answer is not present in the document, "
                            "say that it is not available in the document.\n\n"
                            "DOCUMENT:\n"
                            + st.session_state.document_text
                        )
                    }
                )

            response = st.write_stream(
                get_response_stream(
                    ai_messages
                )
            )

        # Save assistant response

        add_message(
            "assistant",
            response
        )

        # Save conversation

        save_current_chat()

        # Refresh sidebar

        st.rerun()

    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )