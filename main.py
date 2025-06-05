import os
import google.generativeai as genai
import PyPDF2

# --- STEP 1: Configure Gemini API ---
genai.configure(api_key="AIzaSyDvCLv3MsKQv5iXDl-dbTTBubCPeNxA42E")  # Replace with your key

model = genai.GenerativeModel("gemini-1.5-flash")


# --- STEP 2: Read PDF Content ---
def extract_pdf_text(pdf_path):
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print("Error reading PDF:", e)
        return ""


# --- STEP 3: Ask Questions Based on PDF Content ---
def ask_question(pdf_text, question):
    prompt = f"Based on the following book content:\n\n{pdf_text}\n\nAnswer this question:\n{question}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating answer: {e}"


# --- STEP 4: Main Loop ---
def main():
    pdf_path = r"C:\Users\HP\Documents\Python\project\pdf_qa_assistant\self_hel.pdf"

  # Use your actual PDF file
    print("PDF Q&A Assistant - Ask questions about your PDF (type 'exit' to quit)\n")

    pdf_text = extract_pdf_text(pdf_path)
    if not pdf_text:
        print("Failed to load PDF content.")
        return

    while True:
        user_question = input("Ask a question:")
        if user_question.lower() in ['exit', 'quit']:
            break
        answer = ask_question(pdf_text, user_question)
        print("Answer:", answer, "\n")


if __name__ == "__main__":
    main()
