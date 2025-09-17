import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import pandas as pd


class UIComponents:
    @staticmethod
    def render_header():
        """Render the main header"""
        st.set_page_config(
            page_title="AI Resume Analyzer",
            page_icon="📄",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        st.title("🎯 AI Resume Analyzer & Job Matcher")
        st.markdown("""
        Upload your resume and job description to get intelligent matching scores,
        detailed analysis, and personalized improvement suggestions.
        """)

    @staticmethod
    def render_file_upload_section():
        """Render file upload section"""
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📄 Upload Resume")
            resume_file = st.file_uploader(
                "Choose your resume file",
                type=['pdf', 'docx', 'txt'],
                key="resume_upload"
            )

        with col2:
            st.subheader("💼 Job Description")
            job_input_method = st.radio(
                "How would you like to provide the job description?",
                ["Upload File", "Paste Text"],
                key="job_input_method"
            )

            if job_input_method == "Upload File":
                job_file = st.file_uploader(
                    "Choose job description file",
                    type=['pdf', 'docx', 'txt'],
                    key="job_upload"
                )
            else:
                job_file = st.text_area(
                    "Paste job description here",
                    height=200,
                    key="job_text_area"
                )

        return resume_file, job_file, job_input_method

    @staticmethod
    def render_score_dashboard(score_data: Dict[str, Any]):
        """Render the scoring dashboard"""
        st.subheader("📊 Match Analysis Dashboard")

        # Overall Score
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            # Gauge chart for overall score
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=score_data["overall_score"],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Overall Match Score"},
                delta={'reference': 70},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.metric("Experience Match", f"{score_data['experience_match']}%")
            st.metric("Semantic Similarity", f"{score_data['semantic_similarity']}%")

        with col3:
            st.metric("Keyword Density", f"{score_data['keyword_density']}%")

            # Overall score color coding
            score_color = "🟢" if score_data["overall_score"] >= 70 else "🟡" if score_data["overall_score"] >= 50 else "🔴"
            st.metric("Match Quality", f"{score_color}")

    @staticmethod
    def render_skill_analysis(score_data: Dict[str, Any]):
        """Render skill analysis section"""
        st.subheader("🛠️ Skill Analysis")

        # Skill match bar chart
        skill_categories = list(score_data["skill_matches"].keys())
        skill_scores = list(score_data["skill_matches"].values())

        fig = px.bar(
            x=skill_categories,
            y=skill_scores,
            title="Skill Match by Category",
            labels={'x': 'Skill Category', 'y': 'Match Percentage'},
            color=skill_scores,
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Detailed skill breakdown
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📋 Your Skills Found")
            for category, skills in score_data["resume_skills"].items():
                if skills:
                    st.write(f"**{category.title()}:** {', '.join(skills)}")

        with col2:
            st.subheader("🎯 Required Skills")
            for category, skills in score_data["job_skills"].items():
                if skills:
                    st.write(f"**{category.title()}:** {', '.join(skills)}")

    @staticmethod
    def render_improvement_suggestions(suggestions: List[str]):
        """Render improvement suggestions"""
        st.subheader("💡 Improvement Suggestions")

        if not suggestions:
            st.success("🎉 Great job! Your resume is well-matched to this position.")
        else:
            for i, suggestion in enumerate(suggestions, 1):
                st.warning(f"**{i}.** {suggestion}")

    @staticmethod
    def render_detailed_analysis(resume_text: str, job_text: str):
        """Render detailed text analysis"""
        with st.expander("📝 Detailed Text Analysis"):
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Resume Content")
                st.text_area("", value=resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text, height=300, disabled=True)

            with col2:
                st.subheader("Job Description")
                st.text_area("", value=job_text[:1000] + "..." if len(job_text) > 1000 else job_text, height=300, disabled=True)

    @staticmethod
    def render_sidebar_info():
        """Render sidebar with app information"""
        with st.sidebar:
            st.header("ℹ️ About")
            st.markdown("""
            This AI-powered tool analyzes your resume against job descriptions using:

            - **NLP Embeddings**: Semantic similarity analysis
            - **Skill Matching**: Automated skill extraction and comparison
            - **Experience Analysis**: Years of experience evaluation
            - **Keyword Optimization**: ATS-friendly suggestions
            """)

            st.header("📈 Scoring Criteria")
            st.markdown("""
            - **Overall Score**: Weighted combination of all factors
            - **Skill Match**: Category-wise skill alignment
            - **Experience**: Years of experience comparison
            - **Semantic Similarity**: Content similarity using AI
            - **Keyword Density**: Resume-JD keyword overlap
            """)

            st.header("🎯 Score Interpretation")
            st.markdown("""
            - **90-100%**: Excellent match
            - **70-89%**: Good match
            - **50-69%**: Fair match
            - **Below 50%**: Needs improvement
            """)

    @staticmethod
    def render_footer():
        """Render footer"""
        st.markdown("---")
        st.markdown(
            "Built with ❤️ using Streamlit, Sentence Transformers, and ChromaDB | "
            "© 2024 AI Resume Analyzer"
        )