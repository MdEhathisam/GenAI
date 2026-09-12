import logging
import os

import streamlit as st
from google import genai


logger = logging.getLogger(__name__)


def get_api_key() -> str | None:
    """Load the key from Streamlit Cloud secrets or a local environment variable."""
    try:
        return st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return os.getenv("GEMINI_API_KEY")


st.set_page_config(page_title="My Own GPT", page_icon="💬")
st.title("My Own GPT")

api_key = get_api_key()
if api_key:
    api_key = api_key.strip()
if not api_key:
    st.error("Server configuration error: the Gemini API key is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)

uploaded_file = st.file_uploader(
    "Upload a file",
    type=["jpeg", "jpg", "png", "pdf", "txt", "mkv", "mp4", "mp3"],
)
question = st.text_input("What would you like to know about this file?")

if st.button("Send"):
    if uploaded_file is None:
        st.warning("Upload a file before sending.")
    else:
        try:
            with st.spinner("Thinking..."):
                response = client.models.generate_content(
                    # Gemini 2.5 Flash is unavailable for newly created API projects.
                    model="gemini-3.6-flash",
                    contents=[
                        {
                            "role": "user",
                            "parts": [
                                {"text": question.strip() or "Analyze this file."},
                                {
                                    "inline_data": {
                                        "mime_type": uploaded_file.type,
                                        "data": uploaded_file.getvalue(),
                                    }
                                },
                            ],
                        }
                    ],
                )
            st.write(response.text)
        except Exception as error:
            status_code = getattr(error, "code", "unknown")
            logger.error(
                "Gemini file request failed: error_type=%s status_code=%s detail=%s",
                type(error).__name__,
                status_code,
                str(error),
            )
            st.error(
                "Unable to analyze the file right now. "
                f"Server error code: {status_code}."
            )

