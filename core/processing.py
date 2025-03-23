from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from joblib import load
import os
import numpy as np

class ResumeProcessor:
    def __init__(self):
        self.vectorizer = self.load_vectorizer()
        
    def load_vectorizer(self):
        vectorizer_path = os.path.join("models", "vectorizer.pkl")
        try:
            return load(vectorizer_path)
        except FileNotFoundError:
            return TfidfVectorizer(ngram_range=(1, 2), stop_words='english', max_features=5000)

    def process_documents(self, job_desc, resumes):
        # Combine documents for consistent vectorization
        all_docs = [job_desc] + resumes
        
        # Fit or transform using persistent vectorizer
        if not hasattr(self.vectorizer, 'vocabulary_'):
            tfidf_matrix = self.vectorizer.fit_transform(all_docs)
        else:
            tfidf_matrix = self.vectorizer.transform(all_docs)
            
        # Split back into job and resume vectors
        job_vector = tfidf_matrix[0]
        resume_vectors = tfidf_matrix[1:]
        
        return job_vector, resume_vectors