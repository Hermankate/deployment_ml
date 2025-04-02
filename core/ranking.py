# # core/ranking.py
# from sklearn.metrics.pairwise import cosine_similarity
# import requests
# import streamlit as st
# import time

# class Ranker:
#     def __init__(self):
#         self._validate_secrets()
#         self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
#         self.headers = {"Authorization": f"Bearer {st.secrets['secrets']['API_KEY']}"}
#         self.max_retries = 3
#         self.retry_delay = 5
#         self.request_timeout = 30

#     def calculate_rankings(self, job_vector, resume_vectors, raw_resumes, th_good, th_potential):
#         """Calculate rankings with error handling at all levels"""
#         try:
#             similarities = cosine_similarity(job_vector, resume_vectors).flatten()
#             return self._process_candidates(similarities, raw_resumes, th_good, th_potential)
#         except Exception as e:
#             st.error(f"Ranking failed: {str(e)}")
#             return []

#     def _validate_secrets(self):
#         """Validate proper secrets configuration"""
#         if 'secrets' not in st.secrets or 'API_KEY' not in st.secrets['secrets']:
#             st.error("""
#                 Missing API Key configuration! Add to .streamlit/secrets.toml:
                
#                 [secrets]
#                 API_KEY = "your_huggingface_key"
#                 """)
#             st.stop()

#     def _process_candidates(self, similarities, resumes, th_good, th_potential):
#         """Process candidates with error isolation"""
#         ranked = []
#         for idx, (score, resume) in enumerate(zip(similarities, resumes)):
#             try:
#                 analysis = self._get_llm_analysis(resume)
#                 ranked.append(self._create_candidate(idx, score, resume, analysis, th_good, th_potential))
#             except Exception as e:
#                 st.warning(f"Failed to process candidate {idx}: {str(e)}")
#                 ranked.append(self._create_error_entry(idx, resume, str(e)))
        
#         return sorted(ranked, key=lambda x: x['score'], reverse=True)

#     def _create_candidate(self, idx, score, resume, analysis, th_good, th_potential):
#         return {
#             "id": idx,
#             "score": round(score, 2),
#             "category": self._determine_category(score, th_good, th_potential),
#             "analysis": analysis,
#             "resume_text": resume,
#             "error": None
#         }

#     def _create_error_entry(self, idx, resume, error_msg):
#         return {
#             "id": idx,
#             "score": 0.0,
#             "category": "Processing Error",
#             "analysis": error_msg,
#             "resume_text": resume,
#             "error": True
#         }

#     def _determine_category(self, score, th_good, th_potential):
#         if score >= th_good:
#             return "Good Fit"
#         if score >= th_potential:
#             return "Potential Fit"
#         return "No Fit"

#     def _get_llm_analysis(self, text):
#         """Get LLM analysis with robust error handling"""
#         prompt = self._format_prompt(text[:3000])  # Truncate for API safety
        
#         for attempt in range(1, self.max_retries + 1):
#             try:
#                 response = requests.post(
#                     self.api_url,
#                     headers=self.headers,
#                     json={"inputs": prompt},
#                     timeout=self.request_timeout
#                 )
#                 return self._handle_api_response(response)
                
#             except requests.exceptions.RequestException as e:
#                 if attempt == self.max_retries:
#                     return f"Request failed: {str(e)}"
#                 time.sleep(self.retry_delay * attempt)
        
#         return "Max retries exceeded"

#     def _format_prompt(self, text):
#         return f"""Extract from resume in this format:
#         - Skills: comma-separated list
#         - Experience: years and roles
#         - Education: degrees
#         - Certifications: list
        
#         Resume: {text}"""

#     def _handle_api_response(self, response):
#         """Handle different API response scenarios"""
#         if response.status_code == 200:
#             return response.json().get('generated_text', 'No analysis generated')
        
#         if response.status_code == 503:  # Model loading
#             return "Model is loading, try again later"
            
#         return f"API Error {response.status_code}: {response.text[:200]}"
#####################################################################################################

# from sklearn.metrics.pairwise import cosine_similarity
# import requests
# import streamlit as st
# import time

# class Ranker:
#     def __init__(self):
#         self._validate_secrets()
#         self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
#         self.headers = {"Authorization": f"Bearer {st.secrets['secrets']['API_KEY']}"}
#         self.max_retries = 3
#         self.retry_delay = 5
#         self.request_timeout = 30

#     def calculate_rankings(self, job_vector, resume_vectors, raw_resumes, th_good, th_potential):
#         """Calculate rankings with error handling at all levels"""
#         try:
#             similarities = cosine_similarity(job_vector, resume_vectors).flatten()
#             return self._process_candidates(similarities, raw_resumes, th_good, th_potential)
#         except Exception as e:
#             st.error(f"Ranking failed: {str(e)}")
#             return []

#     def _validate_secrets(self):
#         """Validate proper secrets configuration"""
#         if 'secrets' not in st.secrets or 'API_KEY' not in st.secrets['secrets']:
#             st.error("""
#                 Missing API Key configuration! Add to .streamlit/secrets.toml:
                
#                 [secrets]
#                 API_KEY = "your_huggingface_key"
#                 """)
#             st.stop()

#     def _process_candidates(self, similarities, resumes, th_good, th_potential):
#         """Process candidates with error isolation"""
#         ranked = []
#         for idx, (score, resume) in enumerate(zip(similarities, resumes)):
#             try:
#                 analysis = self._get_llm_analysis(resume)
#                 ranked.append(self._create_candidate(idx, score, resume, analysis, th_good, th_potential))
#             except Exception as e:
#                 st.warning(f"Failed to process candidate {idx}: {str(e)}")
#                 ranked.append(self._create_error_entry(idx, resume, str(e)))
        
#         return sorted(ranked, key=lambda x: x['score'], reverse=True)

#     def _create_candidate(self, idx, score, resume, analysis, th_good, th_potential):
#         # Safe name extraction from analysis
#         name = "Unknown"
#         try:
#             if "Candidate Name:" in analysis:
#                 name = analysis.split("Candidate Name:")[1].split("\n")[0].strip()
#         except Exception:
#             pass
        
#         return {
#             "id": idx,
#             "name": name,
#             "score": round(score, 2),
#             "category": self._determine_category(score, th_good, th_potential),
#             "analysis": analysis,
#             "resume_text": resume,
#             "error": None
#         }

#     def _create_error_entry(self, idx, resume, error_msg):
#         return {
#             "id": idx,
#             "name": "Error",
#             "score": 0.0,
#             "category": "Processing Error",
#             "analysis": error_msg,
#             "resume_text": resume,
#             "error": True
#         }

#     def _determine_category(self, score, th_good, th_potential):
#         if score >= th_good:
#             return "Good Fit"
#         if score >= th_potential:
#             return "Potential Fit"
#         return "No Fit"

#     def _get_llm_analysis(self, text):
#         """Get LLM analysis with Mistral-specific handling"""
#         prompt = self._format_prompt(text[:3000])
        
#         for attempt in range(1, self.max_retries + 1):
#             try:
#                 response = requests.post(
#                     self.api_url,
#                     headers=self.headers,
#                     json={"inputs": prompt},
#                     timeout=self.request_timeout
#                 )
#                 return self._handle_api_response(response)
                
#             except requests.exceptions.RequestException as e:
#                 if attempt == self.max_retries:
#                     return f"Request failed: {str(e)}"
#                 time.sleep(self.retry_delay * attempt)
        
#         return "Max retries exceeded"

#     def _format_prompt(self, text):
#         return f"""ANALYZE THIS RESUME AND RETURN STRUCTURED DATA:
#         Candidate Name: [full name]
#         Skills: [comma-separated list]
#         Experience: [years and roles summary]
#         Education: [degrees and institutions]
#         Certifications: [list or none]
        
#         RESUME CONTENT:
#         {text}
        
#         STRUCTURED RESPONSE:"""

#     def _handle_api_response(self, response):
#         """Handle Mistral's list response format"""
#         if response.status_code == 200:
#             response_data = response.json()
            
#             # Handle list format responses
#             if isinstance(response_data, list):
#                 if len(response_data) > 0:
#                     return response_data[0].get('generated_text', 'No analysis generated')
#                 return "Empty response from API"
                
#             # Handle standard object format
#             return response_data.get('generated_text', 'No analysis generated')
        
#         if response.status_code == 503:
#             return "Model is loading, try again later"
            
#         return f"API Error {response.status_code}: {response.text[:200]}"
from sklearn.metrics.pairwise import cosine_similarity
import requests
import streamlit as st
import time
import re

class Ranker:
    def __init__(self, vectorizer):
        self.vectorizer = vectorizer
        self._validate_secrets()
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
        # In Ranker class, change the API URL to:
        self.api_url = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"  # Free tier compatible
        self.headers = {"Authorization": f"Bearer {st.secrets['secrets']['API_KEY']}"}
        self.max_retries = 3
        self.retry_delay = 5
        self.request_timeout = 30

    def calculate_rankings(self, job_vector, resume_vectors, raw_resumes, th_good, th_potential):
        """Calculate rankings with enhanced scoring"""
        try:
            base_scores = cosine_similarity(job_vector, resume_vectors).flatten()
            enhanced_scores = self._enhance_scores(base_scores, raw_resumes)
            return self._process_candidates(enhanced_scores, raw_resumes, th_good, th_potential)
        except Exception as e:
            st.error(f"Ranking failed: {str(e)}")
            return []

    def _enhance_scores(self, base_scores, resumes):
        """Add skill-based scoring enhancements"""
        enhanced = []
        for score, resume in zip(base_scores, resumes):
            analysis = self._get_llm_analysis(resume)
            skill_boost = self._calculate_skill_boost(analysis)
            enhanced.append(score * 0.7 + skill_boost * 0.3)
        return enhanced

    def _calculate_skill_boost(self, analysis):
        """Calculate skill match bonus"""
        try:
            skills_section = analysis.split("Core Skills:")[1].split("\n")[0]
            candidate_skills = [s.strip().lower() for s in skills_section.split(",")]
            job_skills = self.vectorizer.get_feature_names_out()
            matches = len(set(candidate_skills) & set(job_skills))
            return min(matches / 10, 0.3)
        except:
            return 0

    def _validate_secrets(self):
        """Validate secrets configuration"""
        if 'secrets' not in st.secrets or 'API_KEY' not in st.secrets['secrets']:
            st.error("Missing API Key in secrets.toml!")
            st.stop()

    def _process_candidates(self, scores, resumes, th_good, th_potential):
        """Process candidates with error handling"""
        ranked = []
        for idx, (score, resume) in enumerate(zip(scores, resumes)):
            try:
                analysis = self._get_llm_analysis(resume)
                ranked.append(self._create_candidate(idx, score, resume, analysis, th_good, th_potential))
            except Exception as e:
                ranked.append(self._create_error_entry(idx, resume, str(e)))
        return sorted(ranked, key=lambda x: x['score'], reverse=True)

    def _create_candidate(self, idx, score, resume, analysis, th_good, th_potential):
        """Create candidate entry with improved name extraction"""
        name = self._extract_name(analysis, resume)
        return {
            "id": idx,
            "name": name,
            "score": round(score, 2),
            "category": self._determine_category(score, th_good, th_potential),
            "analysis": analysis,
            "resume_text": resume,
            "error": None
        }

    def _extract_name(self, analysis, resume):
        """Extract name using regex patterns"""
        try:
            # Try structured response format
            match = re.search(r"Candidate Name:\s*(.+?)\s*\n", analysis)
            if match: return match.group(1).strip()
            
            # Fallback to resume text parsing
            first_line = resume.split('\n')[0].strip()
            if re.match(r"^[A-Za-z ]+$", first_line):
                return first_line
                
            return "Unknown"
        except:
            return "Unknown"

    def _create_error_entry(self, idx, resume, error_msg):
        return {
            "id": idx,
            "name": "Error",
            "score": 0.0,
            "category": "Processing Error",
            "analysis": error_msg,
            "resume_text": resume,
            "error": True
        }

    def _determine_category(self, score, th_good, th_potential):
        if score >= th_good: return "Good Fit"
        if score >= th_potential: return "Potential Fit"
        return "No Fit"

    def _get_llm_analysis(self, text):
        """Get structured analysis from LLM"""
        prompt = self._format_prompt(text[:3000])
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json={"inputs": prompt},
                    timeout=self.request_timeout
                )
                return self._handle_response(response)
            except requests.RequestException:
                time.sleep(self.retry_delay * (attempt + 1))
        return "Max retries exceeded"

    def _format_prompt(self, text):
        return f"""EXTRACT CANDIDATE PROFILE:
Candidate Name: [Full Name]
Core Skills: [Comma-separated technical skills]
Experience: [Years in relevant roles]
Education: [Highest degree]
Certifications: [List or None]

RESUME CONTENT:
{text}

STRUCTURED RESPONSE:"""

    def _handle_response(self, response):
        """Handle API response formats"""
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list):
                return result[0].get('generated_text', '')
            return result.get('generated_text', '')
        return f"API Error {response.status_code}"
