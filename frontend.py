import streamlit as st
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env
load_dotenv()

# Azure config from .env
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
subscription_key = os.getenv("AZURE_OPENAI_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Initialize client
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

# Streamlit page setup
st.set_page_config(page_title="Azure Chatbot", layout="centered")

st.markdown(
    """
    <style>
        .main {
            padding: 2rem;
            background-color: #f9f9f9;
        }
        .stTextArea, .stButton {
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 Azure OpenAI Chatbot")
st.write("Ask anything and get answers from GPT-4o via Azure.")

# Input area
user_input = st.text_area("Your Question", placeholder="e.g. I am going to Paris, what should I see?", height=120)

if st.button("💬 Ask"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating response..."):
            try:
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=4096,
                    temperature=1.0,
                    top_p=1.0,
                    model=deployment
                )
                st.success("Answer:")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
