import streamlit as st
import requests

st.title('Video Reels')

# Fetch videos
response = requests.get("http://localhost:8000/videos/")
videos = response.json()

for video in videos:
    st.video(video['url'])
    st.write(video['title'])