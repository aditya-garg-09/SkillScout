import streamlit as st
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.document_parser import DocumentParser
from models.embeddings import EmbeddingModel
from models.matcher import ResumeJobMatcher
from components.ui_components import UIComponents


def main():
    # Initialize UI
    UIComponents.render_header()
    UIComponents.render_sidebar_info()

    # Initialize models
    @st.cache_resource
    def load_models():
        embedding_model = EmbeddingModel()
        embedding_model.load_model()
        matcher = ResumeJobMatcher(embedding_model)
        return embedding_model, matcher

    try:
        embedding_model, matcher = load_models()
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        st.stop()

    # File upload section
    resume_file, job_input, job_input_method = UIComponents.render_file_upload_section()

    # Process documents when both are provided
    if resume_file is not None and job_input:
        with st.spinner("🔄 Processing documents..."):
            # Parse resume
            resume_text = DocumentParser.parse_document(resume_file)
            resume_text = DocumentParser.clean_text(resume_text)

            # Parse job description
            if job_input_method == "Upload File":
                job_text = DocumentParser.parse_document(job_input)
            else:
                job_text = job_input

            job_text = DocumentParser.clean_text(job_text)

            if not resume_text or not job_text:
                st.error("❌ Could not extract text from one or both documents. Please check your files.")
                st.stop()

        # Analyze and score
        with st.spinner("🧠 Analyzing match..."):
            try:
                score_data = matcher.generate_comprehensive_score(resume_text, job_text)
                suggestions = matcher.generate_improvement_suggestions(score_data)

                # Display results
                UIComponents.render_score_dashboard(score_data)
                UIComponents.render_skill_analysis(score_data)
                UIComponents.render_improvement_suggestions(suggestions)
                UIComponents.render_detailed_analysis(resume_text, job_text)

                # Store in vector database for future searches
                with st.spinner("💾 Storing for future analysis..."):
                    resume_metadata = {
                        "filename": resume_file.name,
                        "type": "resume",
                        "upload_time": str(st.session_state.get("upload_time", "unknown"))
                    }
                    job_metadata = {
                        "type": "job_description",
                        "upload_time": str(st.session_state.get("upload_time", "unknown"))
                    }

                    embedding_model.store_document(resume_text, resume_metadata, "resume")
                    embedding_model.store_document(job_text, job_metadata, "job_description")

            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.error("Please try again or contact support if the issue persists.")

    else:
        # Show instructions when no files are uploaded
        st.info("👆 Please upload your resume and provide a job description to get started!")

        # Show demo/example section
        with st.expander("📖 How to use this tool"):
            st.markdown("""
            ### Step-by-Step Guide:

            1. **Upload Your Resume**: Upload a PDF, DOCX, or TXT file containing your resume
            2. **Provide Job Description**: Either upload a job description file or paste the text directly
            3. **Get Analysis**: The AI will analyze your resume against the job requirements
            4. **Review Scores**: See detailed matching scores across different categories
            5. **Follow Suggestions**: Use the improvement recommendations to optimize your resume

            ### Tips for Best Results:
            - Ensure your resume is well-formatted and readable
            - Include complete job descriptions with requirements and responsibilities
            - Use clear, professional language in your resume
            - Update your resume based on the suggestions provided
            """)

    # Footer
    UIComponents.render_footer()


if __name__ == "__main__":
    main()