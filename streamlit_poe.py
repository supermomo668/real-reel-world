import streamlit as st
import httpx
import asyncio

# Async function to fetch video
async def fetch_video():
    async with httpx.AsyncClient() as client:
        response = await client.get("")
        return response.content

# Async function to fetch text
async def fetch_text():
    async with httpx.AsyncClient() as client:
        response = await client.get("YOUR_TEXT_ENDPOINT_URL")
        return response.text

# Function to run the async loop for video
def load_video():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_video())

# Function to run the async loop for text
def load_text():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(fetch_text())

# Streamlit UI components
st.title("Your App Title")

col1, col2 = st.columns(2)
with col1:
    if st.button("Refresh Video"):
        video_bytes = load_video()
        st.video(video_bytes)
with col2:
    if st.button("↓ Load Text"):
        text_content = load_text()
        st.session_state['text'] = text_content  # Store in session state

# Load video on app load
if 'video_loaded' not in st.session_state:
    video_bytes = load_video()
    st.session_state['video_loaded'] = True
    st.video(video_bytes)

# Text Editor Interface
st.header("Business Action Plan")
text = st.text_area("", value=st.session_state.get('text', ''), height=300)
