import os
import logging

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
if not api_key:
    st.error("Server configuration error: the Gemini API key is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)

with st.form("question_form"):
    question = st.text_input("Ask anything")
    submitted = st.form_submit_button("Send")

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Thinking..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=question.strip(),
                )
            st.write(response.text)
        except Exception as error:
            # Keep diagnostics in private Streamlit logs; never reveal them to visitors.
            logger.error(
                "Gemini request failed: error_type=%s status_code=%s",
                type(error).__name__,
                getattr(error, "code", "unknown"),
            )
            st.error("Unable to generate a response right now. Please try again later.")
