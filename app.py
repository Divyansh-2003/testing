import streamlit as st
import requests
import json

# Claude API call function
def call_claude_api(api_key, prompt, file_content):
    payload = {
        "prompt": prompt + "\n\n" + file_content,
        "max_tokens_to_sample": 300
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    # ⚠️ Replace with the actual Claude endpoint
    url = "https://api.anthropic.com/v1/complete"

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API call failed with {response.status_code}: {response.text}"}


# Streamlit UI
st.set_page_config(page_title="Claude Doc Analyzer", page_icon="🤖", layout="centered")

st.title("🤖 Claude Document Analyzer")

# Input API key
api_key = st.text_input("Enter your Claude API Key", type="password")

# Input prompt
prompt = st.text_area("Enter your prompt", "Summarize this document in 5 bullet points.")

# File uploader
uploaded_file = st.file_uploader("Upload a document", type=["txt", "md", "json", "py", "csv", "pdf"])

if st.button("Run Analysis"):
    if not api_key:
        st.error("Please provide your Claude API key.")
    elif not prompt:
        st.error("Please provide a prompt.")
    elif not uploaded_file:
        st.error("Please upload a file.")
    else:
        try:
            # For simplicity: read file as text (works for txt, csv, md, etc.)
            file_content = uploaded_file.read().decode("utf-8", errors="ignore")

            # Call API
            result = call_claude_api(api_key, prompt, file_content)

            # Display response
            st.subheader("Claude Output")
            st.json(result)

        except Exception as e:
            st.error(f"Error: {e}")
