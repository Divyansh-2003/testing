import streamlit as st
import requests
import json

st.title("Claude File Analyzer")

# Input fields
api_key = st.text_input("Enter your Claude API Key", type="password")
prompt = st.text_area("Enter your prompt")
uploaded_file = st.file_uploader("Upload a document", type=["txt", "csv", "json", "pdf"])

if st.button("Analyze"):

    if not api_key:
        st.error("API key is required.")
    elif not prompt:
        st.error("Prompt is required.")
    elif not uploaded_file:
        st.error("Please upload a file.")
    else:
        # Read file content
        try:
            file_content = uploaded_file.read().decode("utf-8")
        except Exception:
            st.warning("File could not be decoded as UTF-8. Reading as bytes instead.")
            file_content = str(uploaded_file.read())

        # Prepare request
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        data = {
            "model": "claude-3",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt + "\n\n" + file_content}]
        }

        # Call API
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            st.success("Analysis complete!")
            st.json(result)
        except requests.exceptions.HTTPError as e:
            st.error(f"API call failed: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")
