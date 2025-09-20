import streamlit as st
import sys
import os
import time

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

    # Render analyze button
    analyze_requested = UIComponents.render_analyze_button()

    # Process analysis if button was clicked
    if analyze_requested or st.session_state.get('start_analysis', False):
        # Reset analysis state after processing
        if analyze_requested:
            st.session_state.start_analysis = False

        # Show progress indicator
        UIComponents.render_analysis_progress()

        # Ensure we have both documents
        if resume_file is not None and job_input:
            try:
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
                score_data = matcher.generate_comprehensive_score(resume_text, job_text)
                suggestions = matcher.generate_improvement_suggestions(score_data)

                # Display results
                st.markdown("---")
                st.markdown("## 📊 Analysis Results")

                UIComponents.render_score_dashboard(score_data)
                UIComponents.render_skill_analysis(score_data)
                UIComponents.render_improvement_suggestions(suggestions)
                UIComponents.render_comparison_view(score_data)
                UIComponents.render_detailed_analysis(resume_text, job_text)

                # Store in vector database for future searches
                resume_metadata = {
                    "filename": resume_file.name if resume_file else "text_input",
                    "type": "resume",
                    "upload_time": str(time.time())
                }
                job_metadata = {
                    "type": "job_description",
                    "upload_time": str(time.time())
                }

                embedding_model.store_document(resume_text, resume_metadata, "resume")
                embedding_model.store_document(job_text, job_metadata, "job_description")

                # Success message
                st.success("✅ Analysis complete! Results are displayed above.")

            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.error("Please try again or contact support if the issue persists.")

    else:
        # Show instructions when no analysis has been started
        upload_status = st.session_state.get('upload_status', {})
        if not upload_status.get('both_ready', False):
            st.markdown("---")
            st.info("👆 Please upload your resume and provide a job description to get started!")

            # Show demo/example section
            with st.expander("📖 How to use SkillScout"):
                st.markdown("""
                ### Step-by-Step Guide:

                1. **📄 Upload Your Resume**: Upload a PDF, DOCX, or TXT file containing your resume
                2. **💼 Provide Job Description**: Either upload a job description file or paste the text directly
                3. **🚀 Click Analyze Match**: Start the AI analysis process
                4. **📊 Review Scores**: See detailed matching scores across different categories
                5. **💡 Follow Suggestions**: Use the improvement recommendations to optimize your resume

                ### Tips for Best Results:
                - Ensure your resume is well-formatted and readable
                - Include complete job descriptions with requirements and responsibilities
                - Use clear, professional language in your resume
                - Upload the most recent version of your resume
                - Include specific skills, technologies, and experience years
                """)

    # Footer
    UIComponents.render_footer()


if __name__ == "__main__":
    main()