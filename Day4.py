import streamlit as st

from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not set")
    st.stop()
  
myaibot = genai.Client(api_key=api_key)

st.title("My Own GPT")

question = st.text_input("Ask Anything")

if st.button("Send"):
  response = myaibot.models.generate_content(
  model="gemini-2.5-flash",
  contents = question
  )

  st.write(response.text)
#AIzaSyBe7ia3Bx0RDhIuEHC9TaFYdhgK2kSFbgk
