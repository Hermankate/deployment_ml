# import streamlit as st
# import base64
# import pandas as pd
# import plotly.express as px

# class Visualization:
#     @staticmethod
#     def show_resume_previews(files):
#         st.sidebar.subheader("Resume Previews")
#         for file in files:
#             st.sidebar.write(f"**{file.name}**")
#             if file.type == "application/pdf":
#                 Visualization._show_pdf(file)
#             else:
#                 text = file.getvalue().decode()
#                 st.sidebar.text_area(f"Content", text[:2000], height=250)

#     @staticmethod
#     def _show_pdf(file):
#         base64_pdf = base64.b64encode(file.read()).decode('utf-8')
#         st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width=700 height=500></iframe>', 
#                     unsafe_allow_html=True)

#     @staticmethod
#     def display_results(candidates):
#         st.subheader("Ranked Candidates")
#         for idx, candidate in enumerate(candidates, 1):
#             with st.expander(f"{idx}. {candidate.get('name', 'Unknown')} - Score: {candidate['score']}"):
#                 col1, col2 = st.columns([1, 3])
#                 with col1:
#                     st.metric("Fit Category", candidate['category'])
#                     st.progress(candidate['score'])
#                 with col2:
#                     st.write("**Key Qualifications**")
#                     st.write(candidate['analysis'])

#     @staticmethod
#     def get_download_link(candidates, filename="ranked_candidates.csv"):
#         # Convert list of dicts to DataFrame
#         df = pd.DataFrame([{
#             "Name": c.get('name', 'Unknown'),
#             "Score": c['score'],
#             "Category": c['category'],
#             "Analysis": c['analysis'],
#             "Resume Excerpt": c['resume_text'][:200]  # First 200 chars
#         } for c in candidates])
        
#         csv = df.to_csv(index=False)
#         b64 = base64.b64encode(csv.encode()).decode()
#         return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV Report</a>'
#     @staticmethod
#     def display_historical_results(df):
#         if not df.empty:
#             st.subheader("Historical Rankings")
#             fig = px.histogram(df, x="score", color="fit_category",
#                              title="Score Distribution History")
#             st.plotly_chart(fig)
#             st.dataframe(df)
#         else:
#             st.warning("No historical data available")
import streamlit as st
import base64
import pandas as pd
import plotly.express as px

class Visualization:
    @staticmethod
    def display_results(candidates):
        st.subheader("Ranked Candidates")
        for idx, candidate in enumerate(candidates, 1):
            with st.expander(f"{idx}. {candidate['name']} - Score: {candidate['score']:.2f}"):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric("Fit Category", candidate['category'])
                    st.progress(candidate['score'])
                with col2:
                    st.write("**Key Qualifications**")
                    st.write(candidate['analysis'])

    @staticmethod
    def get_download_link(candidates):
        df = pd.DataFrame([{
            "Name": c['name'],
            "Score": c['score'],
            "Category": c['category'],
            "Skills": "\n".join(c['analysis'].split("Core Skills:")[1].split("\n")[0].split(",")) if "Core Skills:" in c['analysis'] else "",
            "Experience": c['analysis'].split("Experience:")[1].split("\n")[0] if "Experience:" in c['analysis'] else ""
        } for c in candidates])
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="candidates.csv">Download Report</a>'

    @staticmethod
    def show_resume_previews(files):
        st.sidebar.subheader("Resume Previews")
        for file in files:
            with st.sidebar.expander(file.name):
                if file.type == "application/pdf":
                    Visualization._show_pdf(file)
                else:
                    st.text(file.getvalue().decode()[:1000])

    @staticmethod
    def _show_pdf(file):
        base64_pdf = base64.b64encode(file.read()).decode('utf-8')
        st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width=700 height=500></iframe>', unsafe_allow_html=True)