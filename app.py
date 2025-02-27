import streamlit as st
import pandas as pd
import requests
import sqlite3
import pdfplumber
import docx2txt
import io
import base64
import os
from PIL import Image

# Database setup
conn = sqlite3.connect("resumes.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        resume_text TEXT,
        job_description TEXT,
        score REAL
    )
""")
conn.commit()

# Function to extract text from resumes
def extract_text(file):
    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(file)
    return ""

def extract_name(resume_text):
    lines = resume_text.split("\n")
    return lines[0] if lines else "Unknown"

def rank_candidates(resumes, job_desc):
    url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
    api_key = st.secrets.get("API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    ranked_candidates = []
    
    for resume in resumes:
        payload = {"resume_text": resume, "job_description": job_desc}
        response = requests.post(url, json=payload, headers=headers)
        score = response.json().get("score", 0)
        ranked_candidates.append((resume, score))
    
    ranked_candidates.sort(key=lambda x: x[1], reverse=True)
    return ranked_candidates

def show_pdf_as_image(pdf_file):
    """Converts first page of PDF to an image and displays it."""
    with pdfplumber.open(pdf_file) as pdf:
        if pdf.pages:
            first_page = pdf.pages[0]
            image = first_page.to_image()
            img_path = "temp_preview.png"
            image.save(img_path)
            st.image(Image.open(img_path), caption="Preview of Uploaded Resume", use_column_width=True)

def get_table_download_link(df, filename="ranked_candidates.csv", text="Download Ranked Candidates Report"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

# Streamlit UI
st.set_page_config(page_title="AI Resume Screening", layout="wide")
st.title("AI Resume Screening & Ranking System")

st.sidebar.header("Options")
preview_resumes = st.sidebar.checkbox("Preview Uploaded Resumes")

uploaded_cvs = st.file_uploader("Upload Resumes (Multiple Allowed)", type=["pdf", "docx"], accept_multiple_files=True)
job_desc_file = st.file_uploader("Upload Job Description", type=["txt", "docx"])
job_desc_text = st.text_area("Or type the Job Description manually")

if job_desc_file:
    job_desc_text = extract_text(job_desc_file)

if uploaded_cvs and preview_resumes:
    st.subheader("Resume Previews:")
    for file in uploaded_cvs:
        st.write(f"**Previewing:** {file.name}")
        if file.type == "application/pdf":
            show_pdf_as_image(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            st.text_area(f"Extracted Text from {file.name}:", extract_text(file), height=250)

if uploaded_cvs and job_desc_text:
    st.subheader("Processing Resumes...")
    
    resumes = [extract_text(cv) for cv in uploaded_cvs]
    ranked_candidates = rank_candidates(resumes, job_desc_text)

    cursor.execute("DELETE FROM candidates")
    conn.commit()
    
    results_list = []
    
    st.subheader("Ranked Candidates:")
    for i, (resume, score) in enumerate(ranked_candidates):
        name = extract_name(resume)
        st.write(f"**{i+1}. {name} **")

        cursor.execute("INSERT INTO candidates (name, resume_text, job_description, score) VALUES (?, ?, ?, ?)", 
                       (name, resume, job_desc_text, score))
        conn.commit()
    
        results_list.append({"Candidate Name": name, "Score": score})
    
    results_df = pd.DataFrame(results_list)
    
    st.markdown(get_table_download_link(results_df), unsafe_allow_html=True)

if st.button("Show Previous Results"):
    cursor.execute("SELECT name, score FROM candidates ORDER BY score DESC")
    results = cursor.fetchall()
    
    if results:
        results_df = pd.DataFrame(results, columns=["Candidate Name", "Score"])
        st.dataframe(results_df)
        st.markdown(get_table_download_link(results_df), unsafe_allow_html=True)
    else:
        st.warning("No previous results found.")

conn.close()
