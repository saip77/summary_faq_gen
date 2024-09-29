import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Configure API key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=api_key)

prompt = """You are a YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and then from the summarized text you will be providing FAQs. 
Please provide the FAQs  """

# Function to extract transcript from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " ".join(i["text"] for i in transcript_text)
        return transcript
    except Exception as e:
        raise e

# Function to generate summary using Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.title("Summary and FAQs Generator")
youtube_link = st.text_input("Enter Video Link:")

if st.button("Get Summary and FAQs"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## FAQs:")
        st.write(summary)