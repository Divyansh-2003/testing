import os
import pandas as pd
import docx
import pdfplumber
import streamlit as st
from openai import OpenAI

# Streamlit frontend
st.set_page_config(page_title="Document Analyzer (OpenAI)", page_icon="📄", layout="centered")

st.title("📄 OpenAI Document Analyzer")

# API key input
api_key = st.text_input("Enter your OpenAI API Key", type="password")

# File upload
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt", "csv", "xlsx"])

# User prompt input
user_prompt = st.text_area("Enter your analysis instructions / prompt:")

# Function to extract text
def extract_text(file):
    ext = file.name.split(".")[-1].lower()

    if ext == "pdf":
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif ext == "docx":
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    elif ext == "txt":
        return file.read().decode("utf-8")

    elif ext == "csv":
        df = pd.read_csv(file)
        return df.to_string()

    elif ext == "xlsx":
        df = pd.read_excel(file)
        return df.to_string()

    return "Unsupported file type."

# Analyze button
if st.button("Analyze"):
    if not api_key:
        st.error("⚠️ Please enter your API key.")
    elif not uploaded_file:
        st.error("⚠️ Please upload a document.")
    elif not user_prompt.strip():
        st.error("⚠️ Please enter your prompt.")
    else:
        # Extract file content
        content = extract_text(uploaded_file)

        # Combine user prompt + document
        full_prompt = f"""
{user_prompt}

Document Content:
{content}
"""

        try:
            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model="gpt-4o-mini",   # you can use gpt-4o or gpt-3.5-turbo
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=800
            )

            st.subheader("✅ Analysis Result:")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"API call failed: {e}")
