import streamlit as st
from PyPDF2 import PdfReader
from document_qa import query_document
import re
import pandas as pd
import os

# Helper function to clean and format PDF text
def clean_pdf_text(raw_text):
    text = re.sub(r'\n+', '\n', raw_text)
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if line.strip():
            if cleaned_lines and not line.endswith(('.', '!', '?')):
                cleaned_lines[-1] += " " + line.strip()
            else:
                cleaned_lines.append(line.strip())
    formatted_text = "\n\n".join(cleaned_lines)
    return formatted_text

# Streamlit app configuration
st.set_page_config(page_title="Smart Study Planner", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = "Home"

# Sidebar options
options = ["Home", "Document Q&A", "Study Planner"]
selected_option = st.sidebar.radio("Go to", options)
st.session_state.selected_option = selected_option

# Main content layout
if st.session_state.selected_option == "Home":
    st.title("Welcome to the Smart Study Planner")
    st.write("""
        ### Home Page
        This is your smart study assistant that will help you plan and organize your study sessions.
        
        ### How to Use:
        - **Document Q&A**: Upload a document and ask questions to extract relevant information.
        - **Study Planner**: Plan your study sessions and set goals.
    """)

elif st.session_state.selected_option == "Document Q&A":
    st.title("📄 Document Question and Answer")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file:
        reader = PdfReader(uploaded_file)
        raw_text = ""
        for page in reader.pages:
            raw_text += page.extract_text()

        # Clean and format extracted text
        cleaned_text = clean_pdf_text(raw_text)
        st.text_area("Document Content", cleaned_text, height=300)

        # User input for question
        user_query = st.text_input("Ask a Question about the document:")

        if user_query:
            # Get answer from OpenAI model
            answer, doc_text = query_document(cleaned_text, user_query)
            
            # Display the result with better formatting
            st.subheader("Answer:")
            st.write(f"**Question:** {user_query}")
            st.write(f"**Answer:** {answer}")
            st.write(f"**Relevant Text from Document:** {doc_text}")
        
        # Read and display the Q&A history from the CSV file
        if os.path.exists('qa_log.csv'):
            qa_df = pd.read_csv('qa_log.csv')
            st.subheader("Q&A History")
            st.dataframe(qa_df)  # Display the CSV data as a table

elif st.session_state.selected_option == "Study Planner":
    st.title("📅 Study Planner")
    st.write("This feature is under development!")