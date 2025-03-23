# # import streamlit as st
# # import pandas as pd
# # import requests
# # import sqlite3
# # import pdfplumber
# # import docx2txt
# # import io
# # import base64
# # import os
# # import joblib
# # from PIL import Image

# # # Load the trained model (Replace 'model.pkl' with your actual model file)
# # model = joblib.load("resume_ranker.pkl")  
# # # Database setup
# # conn = sqlite3.connect("resumes.db")
# # cursor = conn.cursor()

# # cursor.execute("""
# #     CREATE TABLE IF NOT EXISTS candidates (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         name TEXT,
# #         resume_text TEXT,
# #         job_description TEXT,
# #         local_score REAL,
# #         llama_score REAL,
# #         final_score REAL
# #     )
# # """)
# # conn.commit()

# # # Function to extract text from resumes
# # def extract_text(file):
# #     if file.type == "application/pdf":
# #         with pdfplumber.open(file) as pdf:
# #             return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
# #     elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
# #         return docx2txt.process(file)
# #     return ""

# # def extract_name(resume_text):
# #     lines = resume_text.split("\n")
# #     return lines[0] if lines else "Unknown"

# # # Function to rank candidates using both trained model & Llama API
# # # Load the trained model and vectorizer
# # try:
# #     model = joblib.load("resume_ranker.pkl")  
# #     vectorizer = joblib.load("tfidf_vectorizer.pkl")  
# # except Exception as e:
# #     st.error(f"Error loading model/vectorizer: {e}")
# #     st.stop()

# # # Function to rank candidates using both trained model & Llama API
# # def rank_candidates(resumes, job_desc):
# #     llama_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
# #     api_key = st.secrets.get("API_KEY")
# #     headers = {"Authorization": f"Bearer {api_key}"}

# #     ranked_candidates = []
    
# #     # Transform job description text
# #     job_desc_tfidf = vectorizer.transform([job_desc])

# #     for resume in resumes:
# #         if not resume.strip():
# #             continue  # Skip empty resumes

# #         # Vectorize resume text
# #         resume_tfidf = vectorizer.transform([resume])
# #         print("Resume TF-IDF Shape:", resume_tfidf.shape) 
# #         # Local Model Score (Ensure it's a 2D array)
# #         local_score = model.predict_proba(resume_tfidf)[:, 1][0] 

# #         # Llama API Score
# #         payload = {"resume_text": resume, "job_description": job_desc}
# #         response = requests.post(llama_url, json=payload, headers=headers)
# #         llama_score = response.json().get("score", 0)

# #         # Combine Scores
# #         final_score = (0.6 * local_score) + (0.4 * llama_score)  # Adjust weights if needed

# #         ranked_candidates.append((resume, local_score, llama_score, final_score))

# #     # Sort by final score
# #     ranked_candidates.sort(key=lambda x: x[3], reverse=True)
# #     return ranked_candidates

# # def show_pdf_as_image(pdf_file):
# #     """Converts first page of PDF to an image and displays it."""
# #     with pdfplumber.open(pdf_file) as pdf:
# #         if pdf.pages:
# #             first_page = pdf.pages[0]
# #             image = first_page.to_image()
# #             img_path = "temp_preview.png"
# #             image.save(img_path)
# #             st.image(Image.open(img_path), caption="Preview of Uploaded Resume", use_column_width=True)

# # def get_table_download_link(df, filename="ranked_candidates.csv", text="Download Ranked Candidates Report"):
# #     csv = df.to_csv(index=False)
# #     b64 = base64.b64encode(csv.encode()).decode()
# #     return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

# # # Streamlit UI
# # st.set_page_config(page_title="AI Resume Screening", layout="wide")
# # st.title("AI Resume Screening & Ranking System")

# # st.sidebar.header("Options")
# # preview_resumes = st.sidebar.checkbox("Preview Uploaded Resumes")

# # uploaded_cvs = st.file_uploader("Upload Resumes (Multiple Allowed)", type=["pdf", "docx"], accept_multiple_files=True)
# # job_desc_file = st.file_uploader("Upload Job Description", type=["txt", "docx"])
# # job_desc_text = st.text_area("Or type the Job Description manually")

# # if job_desc_file:
# #     job_desc_text = extract_text(job_desc_file)

# # if uploaded_cvs and preview_resumes:
# #     st.subheader("Resume Previews:")
# #     for file in uploaded_cvs:
# #         st.write(f"**Previewing:** {file.name}")
# #         if file.type == "application/pdf":
# #             show_pdf_as_image(file)
# #         elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
# #             st.text_area(f"Extracted Text from {file.name}:", extract_text(file), height=250)

# # if uploaded_cvs and job_desc_text:
# #     st.subheader("Processing Resumes...")
    
# #     resumes = [extract_text(cv) for cv in uploaded_cvs]
# #     ranked_candidates = rank_candidates(resumes, job_desc_text)

# #     cursor.execute("DELETE FROM candidates")
# #     conn.commit()
    
# #     results_list = []
    
# #     st.subheader("Ranked Candidates:")
# #     for i, (resume, local_score, llama_score, final_score) in enumerate(ranked_candidates):
# #         name = extract_name(resume)
# #         st.write(f"**{i+1}. {name} - Final Score: {final_score} (Local: {local_score}, Llama: {llama_score})**")

# #         cursor.execute("INSERT INTO candidates (name, resume_text, job_description, local_score, llama_score, final_score) VALUES (?, ?, ?, ?, ?, ?)", 
# #                        (name, resume, job_desc_text, local_score, llama_score, final_score))
# #         conn.commit()
    
# #         results_list.append({"Candidate Name": name, "Local Score": local_score, "Llama Score": llama_score, "Final Score": final_score})
    
# #     results_df = pd.DataFrame(results_list)
    
# #     st.markdown(get_table_download_link(results_df), unsafe_allow_html=True)

# # if st.button("Show Previous Results"):
# #     cursor.execute("SELECT name, local_score, llama_score, final_score FROM candidates ORDER BY final_score DESC")
# #     results = cursor.fetchall()
    
# #     if results:
# #         results_df = pd.DataFrame(results, columns=["Candidate Name", "Local Score", "Llama Score", "Final Score"])
# #         st.dataframe(results_df)
# #         st.markdown(get_table_download_link(results_df), unsafe_allow_html=True)
# #     else:
# #         st.warning("No previous results found.")

# # conn.close()

# ################################################################################################
# import streamlit as st
# import base64
# import os
# from dotenv import load_dotenv
# from core.database import DatabaseManager
# from core.processing import ResumeProcessor
# from core.ranking import Ranker
# from utils.file_handling import FileHandler
# from utils.visualization import Visualization

# # Initialize components
# load_dotenv()
# db = DatabaseManager()
# processor = ResumeProcessor()
# ranker = Ranker()
# file_handler = FileHandler()
# viz = Visualization()

# # Streamlit UI Configuration
# st.set_page_config(page_title="AI Resume Screening", layout="wide")
# st.title("AI Resume Screening & Ranking System")

# def main():
#     st.sidebar.header("Processing Options")
#     preview_resumes = st.sidebar.checkbox("Preview Uploaded Resumes")
#     threshold_good = st.sidebar.slider("Good Fit Threshold", 0.0, 1.0, 0.7)
#     threshold_potential = st.sidebar.slider("Potential Fit Threshold", 0.0, 1.0, 0.4)

#     uploaded_cvs = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
#     job_desc_file = st.file_uploader("Upload Job Description", type=["txt", "docx"])
#     job_desc_text = st.text_area("Or type the Job Description manually")

#     if job_desc_file:
#         job_desc_text = file_handler.extract_text(job_desc_file)

#     if uploaded_cvs and preview_resumes:
#         viz.show_resume_previews(uploaded_cvs)

#     if uploaded_cvs and job_desc_text:
#         with st.spinner("Processing Resumes..."):
#             # Process documents
#             resumes = [file_handler.extract_text(cv) for cv in uploaded_cvs]
#             job_vector, resume_vectors = processor.process_documents(job_desc_text, resumes)
            
#             # Calculate rankings
#             ranked_candidates = ranker.calculate_rankings(job_vector, resume_vectors, resumes,
#                                                          threshold_good, threshold_potential)
            
#             # Store and display results
#             db.store_results(ranked_candidates, job_desc_text)
#             viz.display_results(ranked_candidates)
            
#             # Show download option
#             st.markdown(viz.get_download_link(ranked_candidates), unsafe_allow_html=True)

#     if st.button("Show Historical Results"):
#         historical_results = db.get_historical_results()
#         viz.display_historical_results(historical_results)

# if __name__ == "__main__":
#     main()





# import streamlit as st
# import base64
# import pandas as pd
# from core.database import DatabaseManager
# from core.processing import ResumeProcessor
# from core.ranking import Ranker
# from utils.file_handling import FileHandler
# from utils.visualization import Visualization

# # Initialize components
# db = DatabaseManager()
# processor = ResumeProcessor()
# ranker = Ranker()
# file_handler = FileHandler()
# viz = Visualization()

# # Streamlit UI Configuration
# st.set_page_config(page_title="AI Resume Screening", layout="wide")
# st.title("AI Resume Screening & Ranking System")

# def main():
#     st.sidebar.header("Processing Options")
#     preview_resumes = st.sidebar.checkbox("Preview Uploaded Resumes")
#     threshold_good = st.sidebar.slider("Good Fit Threshold", 0.0, 1.0, 0.7)
#     threshold_potential = st.sidebar.slider("Potential Fit Threshold", 0.0, 1.0, 0.4)

#     # File uploaders
#     uploaded_cvs = st.file_uploader("Upload Resumes", 
#                                    type=["pdf", "docx"], 
#                                    accept_multiple_files=True,
#                                    help="Max file size: 5MB")
#     job_desc_file = st.file_uploader("Upload Job Description", 
#                                     type=["txt", "docx"])
#     job_desc_text = st.text_area("Or type the Job Description manually")

#     # Process job description
#     if job_desc_file:
#         job_desc_text = file_handler.extract_text(job_desc_file)

#     # Show previews
#     if uploaded_cvs and preview_resumes:
#         viz.show_resume_previews(uploaded_cvs)

#     # Main processing
#     if uploaded_cvs and job_desc_text:
#         with st.spinner("Processing Resumes..."):
#             valid_resumes = []
#             for cv in uploaded_cvs:
#                 text = file_handler.extract_text(cv)
#                 if text.strip():
#                     valid_resumes.append(text)
#                 else:
#                     st.warning(f"Skipped invalid/corrupted file: {cv.name}")

#             if valid_resumes:
#                 try:
#                     job_vector, resume_vectors = processor.process_documents(job_desc_text, valid_resumes)
#                     ranked_candidates = ranker.calculate_rankings(job_vector, resume_vectors, valid_resumes,
#                                                                 threshold_good, threshold_potential)
#                     db.store_results(ranked_candidates, job_desc_text)
#                     viz.display_results(ranked_candidates)
                    
#                     # Download handling
#                     download_df = pd.DataFrame([
#                         {
#                             "Name": c.get('name', 'Unknown'),
#                             "Score": c['score'],
#                             "Category": c['category'],
#                             "Analysis": c['analysis'],
#                             "Resume Excerpt": c['resume_text'][:200]
#                         } for c in ranked_candidates
#                     ])
#                     st.markdown(viz.get_download_link(download_df), unsafe_allow_html=True)
                    
#                 except Exception as e:
#                     st.error(f"Processing failed: {str(e)}")
#             else:
#                 st.warning("No valid resumes found in uploaded files")

#     # Historical results
#     if st.button("Show Historical Results"):
#         historical_results = db.get_historical_results()
#         viz.display_historical_results(historical_results)

# if __name__ == "__main__":
#     main()
import streamlit as st
import pandas as pd
from core.database import DatabaseManager
from core.processing import ResumeProcessor
from core.ranking import Ranker
from utils.file_handling import FileHandler
from utils.visualization import Visualization

# Initialize components
db = DatabaseManager()
processor = ResumeProcessor()
file_handler = FileHandler()
viz = Visualization()

def main():
    # Streamlit UI Configuration (kept original layout)
    st.set_page_config(page_title="AI Resume Screening", layout="wide")
    st.title("AI Resume Screening & Ranking System")

    st.sidebar.header("Processing Options")
    preview_resumes = st.sidebar.checkbox("Preview Uploaded Resumes")
    threshold_good = st.sidebar.slider("Good Fit Threshold", 0.0, 1.0, 0.4)  # Adjusted default
    threshold_potential = st.sidebar.slider("Potential Fit Threshold", 0.0, 1.0, 0.2)  # Adjusted default

    # File uploaders (original structure)
    uploaded_cvs = st.file_uploader("Upload Resumes", 
                                   type=["pdf", "docx"], 
                                   accept_multiple_files=True,
                                   help="Max file size: 5MB")
    job_desc_file = st.file_uploader("Upload Job Description", 
                                    type=["txt", "docx"])
    job_desc_text = st.text_area("Or type the Job Description manually")

    # Process job description (original)
    if job_desc_file:
        job_desc_text = file_handler.extract_text(job_desc_file)

    # Show previews (original)
    if uploaded_cvs and preview_resumes:
        viz.show_resume_previews(uploaded_cvs)

    # Main processing with functional improvements
    if uploaded_cvs and job_desc_text:
        with st.spinner("Processing Resumes..."):
            valid_resumes = []
            for cv in uploaded_cvs:
                try:
                    text = file_handler.extract_text(cv)
                    if text and text.strip():
                        valid_resumes.append(text)
                    else:
                        st.warning(f"Skipped invalid/corrupted file: {cv.name}")
                except Exception as e:
                    st.error(f"Error processing {cv.name}: {str(e)}")

            if valid_resumes:
                try:
                    # Initialize ranker with processor's vectorizer
                    ranker = Ranker(processor.vectorizer)
                    
                    # Process documents
                    job_vector, resume_vectors = processor.process_documents(job_desc_text, valid_resumes)
                    
                    # Calculate rankings with enhanced scoring
                    ranked_candidates = ranker.calculate_rankings(
                        job_vector, resume_vectors, valid_resumes,
                        threshold_good, threshold_potential
                    )
                    
                    # Store results with improved error handling
                    db.store_results(ranked_candidates, job_desc_text)
                    
                    # Display results with name extraction
                    viz.display_results(ranked_candidates)
                    
                    # Enhanced download handling
                    st.markdown(viz.get_download_link(ranked_candidates), unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Processing failed: {str(e)}")
            else:
                st.warning("No valid resumes found in uploaded files")

    # Historical results (original)
    if st.button("Show Historical Results"):
        historical_results = db.get_historical_results()
        viz.display_historical_results(historical_results)

if __name__ == "__main__":
    main()