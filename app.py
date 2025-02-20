import streamlit as st
import os

from llm import error_samples, get_ai_response


st.title("Launch Assistant🚀")
st.write("Share your logs.")

st.sidebar.header("Select a Sample Error:")

if "selected_error" not in st.session_state:
    st.session_state.selected_error = None

st.sidebar.markdown(
    """
    <style>
        .stButton > button {
            width: 100%;
            text-align: center;
            padding: 1px;
            margin: 2px 0;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
            border: none;
        }
        .stButton > button:hover {
            background-color: #ddd;
        }
    </style>
    """,
    unsafe_allow_html=True
)

selected_error_text = None

for error_name, error_text in error_samples.items():
    if st.sidebar.button(error_name, key=error_name):
        st.session_state.selected_error = error_text
        selected_error_text = error_text

user_input = st.chat_input("Type/Paste your logs here OR Click the Sample logs from the Sidepanel")

if selected_error_text:
    user_input = selected_error_text

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        for chunk in get_ai_response(user_input):
            full_response += chunk
            response_container.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
