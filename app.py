import os
import streamlit as st
import PyPDF2
import google.generativeai as genai

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyDvCLv3MsKQv5iXDl-dbTTBubCPeNxA42E")  # Replace with your key
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Extract Text from PDF ---
def extract_pdf_text(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# --- Ask Gemini AI ---
def ask_question(pdf_text, question):
    if not question.strip():
        return "Please enter a question."

    prompt = f"Based on the following book content:\n\n{pdf_text}\n\nAnswer this question:\n{question}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating answer: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="PDF Q&A Assistant", layout="centered")

st.title("📘 PDF Q&A Assistant")
st.markdown("Upload a PDF and ask questions based on its content. Powered by **Gemini AI**.")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    pdf_text = extract_pdf_text(uploaded_file)
    question = st.text_input("Ask a question based on the PDF content:")

    if question:
        with st.spinner("Thinking..."):
            answer = ask_question(pdf_text, question)
        st.markdown("### 📖 Answer:")
        st.write(answer)
