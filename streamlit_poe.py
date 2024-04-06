import streamlit as st
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Function to initialize and train the bot
def initialize_bot():
    bot = ChatBot("Poe Bot")
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train("chatterbot.corpus.english")
    return bot

# Function to interact with the bot
def chat_with_bot(bot, video_url):
    response = bot.get_response(video_url)
    return str(response)

# Function to create the Streamlit app
def create_app():
    # Create a Streamlit app
    st.title("Poe Bot with Video Input")

    # Initialize the bot
    bot = initialize_bot()

    # Add a video input field
    video_url = st.text_input("Enter the video URL")

    # Check if the video URL is provided
    if video_url:
        # Process the video URL and get the response from the bot
        response = chat_with_bot(bot, video_url)

        # Display the response
        st.text_area("Bot Response", value=response, height=200)

    # Run the Streamlit app
    if __name__ == "__main__":
        st.set_page_config(layout="wide")
        st.sidebar.title("Bot Application")
        st.sidebar.write("Enter a video URL to chat with the bot.")

# Call the create_app function to start the Streamlit app
create_app()