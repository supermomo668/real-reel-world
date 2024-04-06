"""Home page of streamlit application"""
import streamlit as st
st.title("POE Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # if message["role"] == "assistant":
        #     st.video("demo_resources/sample_video.mp4 (240p).mp4")
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
        st.video("demo_videos/new_download.mp4")
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})