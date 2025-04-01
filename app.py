
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