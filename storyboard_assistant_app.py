
import streamlit as st
import openai
import textwrap

# Set up the page
st.set_page_config(page_title="Storyboard Assistant", layout="wide")
st.title("Storyboard Assistant")

# API Key (hardcoded for demo - replace with your own key when deploying)
openai.api_key = "sk-..."  # Replace with your actual key

# User Inputs
week = st.text_input("Enter Week Number", "")
video = st.text_input("Enter Video Number", "")
transcript = st.text_area("Paste the full transcript here", height=400)

if st.button("Generate Storyboard"):
    if not (week and video and transcript):
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Generating storyboard..."):
            # Simplified prompt - replace with your custom prompt logic
            system_prompt = """You are a professional video editor creating storyboards from transcripts.
- Chunk the transcript into logical video frames.
- Assign a frame type to each chunk:
    * Wide: only at start/end or for powerful standalone lines.
    * Wide with Text: for most content; include headers, subheaders, parallel bullets.
    * Null: for complex frameworks or big ideas.
    * Bleed: if the chunk is under 50 words and impactful.
- Suggest a Shutterstock image keyword for each frame (no editorial images).
- Ensure the entire transcript is covered.
Output a clear and clean .txt storyboard for download.
"""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.4
            )

            storyboard_output = response.choices[0].message["content"]

            file_name = f"Week{week}.Video{video}.txt"
            st.download_button("Download Storyboard", storyboard_output, file_name=file_name, mime="text/plain")
            st.success("Storyboard ready!")
