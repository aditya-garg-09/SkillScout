import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import pandas as pd
import time


class UIComponents:
    @staticmethod
    def inject_responsive_css():
        """Inject responsive CSS for better UI adaptation"""
        st.markdown("""
        <style>
        /* Responsive layout adjustments */
        .main .block-container {
            padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        /* Modern card styling */
        .upload-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            color: white;
        }

        .upload-card h3 {
            color: white !important;
            margin-bottom: 1rem;
        }

        /* Analysis button styling */
        .analyze-button {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            color: white;
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            cursor: pointer;
            width: 100%;
            margin: 1rem 0;
        }

        .analyze-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }

        /* Sidebar adaptation */
        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }

        /* Status indicators */
        .status-indicator {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            margin: 0.5rem 0;
            font-weight: 600;
        }

        .status-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .status-warning {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }

        .status-info {
            background-color: #cce7ff;
            color: #004085;
            border: 1px solid #99d6ff;
        }

        /* Premium card styling */
        .premium-card {
            background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            margin: 1rem 0;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        .premium-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        }

        .metric-card {
            background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            text-align: center;
            margin: 0.5rem;
            border: 1px solid rgba(255,255,255,0.3);
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        }

        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }

        .metric-label {
            color: #495057;
            font-size: 0.9rem;
            font-weight: 500;
        }

        /* Premium analyze button */
        .premium-analyze-button {
            background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 3rem;
            border: none;
            border-radius: 50px;
            font-size: 1.3rem;
            font-weight: 700;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            transition: all 0.3s ease;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
            min-width: 300px;
            min-height: 60px;
        }

        .premium-analyze-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
            background: linear-gradient(45deg, #5a67d8 0%, #667eea 100%);
        }

        .premium-analyze-button:disabled {
            background: linear-gradient(45deg, #a0aec0 0%, #cbd5e0 100%);
            cursor: not-allowed;
            transform: none;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        /* Suggestion cards */
        .suggestion-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 5px solid #667eea;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            color: #2d3748;
            font-weight: 500;
            line-height: 1.6;
        }

        .suggestion-card.success {
            border-left-color: #48bb78;
            background: linear-gradient(135deg, #f0fff4 0%, #ffffff 100%);
        }

        .suggestion-card.warning {
            border-left-color: #ed8936;
            background: linear-gradient(135deg, #fffaf0 0%, #ffffff 100%);
        }

        .suggestion-card.info {
            border-left-color: #4299e1;
            background: linear-gradient(135deg, #ebf8ff 0%, #ffffff 100%);
        }

        /* Analysis grid */
        .analysis-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        /* Enhanced button container */
        .button-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 2rem 0;
            padding: 2rem;
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            border-radius: 20px;
            border: 2px dashed #cbd5e0;
        }
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_header():
        """Render the modern header with responsive design"""
        st.set_page_config(
            page_title="SkillScout - AI Resume Analyzer",
            page_icon="🎯",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Inject responsive CSS
        UIComponents.inject_responsive_css()

        # Modern header with gradient background
        st.markdown("""
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                    padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">🎯 SkillScout</h1>
            <h3 style="color: #f0f0f0; margin: 0.5rem 0 0 0; font-weight: 300;">
                AI-Powered Resume Analysis & Job Matching
            </h3>
            <p style="color: #e0e0e0; margin: 1rem 0 0 0; font-size: 1.1rem;">
                Get intelligent matching scores, detailed analysis, and personalized improvement suggestions
            </p>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_upload_status(file_name, file_type):
        """Render upload status indicator"""
        if file_name:
            st.markdown(f"""
            <div class="status-indicator status-success">
                ✅ {file_type} uploaded: {file_name}
            </div>
            """, unsafe_allow_html=True)
            return True
        return False

    @staticmethod
    def render_file_upload_section():
        """Render modern file upload section with cards and responsive design"""
        st.markdown("### 📂 Document Upload")

        # Responsive columns that adapt to sidebar state
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            # Resume upload card
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;">
                <h3 style="color: white; margin: 0 0 1rem 0;">📄 Resume Upload</h3>
            </div>
            """, unsafe_allow_html=True)

            resume_file = st.file_uploader(
                "Choose your resume file (PDF, DOCX, TXT)",
                type=['pdf', 'docx', 'txt'],
                key="resume_upload",
                help="Upload your most recent resume for analysis"
            )

            # Resume upload status
            resume_uploaded = UIComponents.render_upload_status(
                resume_file.name if resume_file else None, "Resume"
            )

        with col2:
            # Job description card
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
                        padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem;">
                <h3 style="color: white; margin: 0 0 1rem 0;">💼 Job Description</h3>
            </div>
            """, unsafe_allow_html=True)

            job_input_method = st.radio(
                "How would you like to provide the job description?",
                ["Upload File", "Paste Text"],
                key="job_input_method",
                horizontal=True
            )

            if job_input_method == "Upload File":
                job_file = st.file_uploader(
                    "Choose job description file (PDF, DOCX, TXT)",
                    type=['pdf', 'docx', 'txt'],
                    key="job_upload",
                    help="Upload the job posting or description"
                )
                job_uploaded = UIComponents.render_upload_status(
                    job_file.name if job_file else None, "Job Description"
                )
            else:
                job_file = st.text_area(
                    "Paste job description here",
                    height=200,
                    key="job_text_area",
                    placeholder="Paste the complete job description including requirements, responsibilities, and qualifications..."
                )
                job_uploaded = bool(job_file and len(job_file.strip()) > 50)
                if job_uploaded:
                    st.markdown("""
                    <div class="status-indicator status-success">
                        ✅ Job description text ready for analysis
                    </div>
                    """, unsafe_allow_html=True)

        # Store upload status in session state for the analyze button
        if 'upload_status' not in st.session_state:
            st.session_state.upload_status = {}

        st.session_state.upload_status['resume'] = resume_uploaded
        st.session_state.upload_status['job'] = job_uploaded
        st.session_state.upload_status['both_ready'] = resume_uploaded and job_uploaded

        return resume_file, job_file, job_input_method

    @staticmethod
    def render_analyze_button():
        """Render the premium analyze button with enhanced styling and positioning"""
        # Check if both files are ready
        upload_status = st.session_state.get('upload_status', {})
        both_ready = upload_status.get('both_ready', False)

        if both_ready:
            # Premium button container positioned near uploads
            st.markdown("""
            <div class="button-container">
                <div style="text-align: center;">
                    <h3 style="margin-bottom: 1rem; color: #4a5568;">🎯 Ready to Analyze</h3>
                    <p style="color: #718096; margin-bottom: 2rem;">Your documents are uploaded and validated. Start the AI analysis!</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Create centered premium button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                # Use custom HTML button for premium styling
                button_clicked = st.button("🚀 Analyze Match", key="analyze_button", type="primary")

                if button_clicked:
                    st.session_state.start_analysis = True
                    st.session_state.analysis_progress = 0
                    return True

                # Add custom styling to the button
                st.markdown("""
                <style>
                div.stButton > button:first-child {
                    background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 1rem 3rem;
                    border: none;
                    border-radius: 50px;
                    font-size: 1.3rem;
                    font-weight: 700;
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    min-width: 300px;
                    min-height: 60px;
                    margin: 0 auto;
                    display: block;
                }

                div.stButton > button:first-child:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
                    background: linear-gradient(45deg, #5a67d8 0%, #667eea 100%);
                }
                </style>
                """, unsafe_allow_html=True)

        else:
            # Show what's needed with premium styling
            resume_status = "✅" if upload_status.get('resume') else "❌"
            job_status = "✅" if upload_status.get('job') else "❌"

            st.markdown(f"""
            <div class="button-container">
                <div style="text-align: center;">
                    <h3 style="margin-bottom: 1rem; color: #4a5568;">📋 Upload Requirements</h3>
                    <div style="margin: 1rem 0;">
                        <span style="font-size: 1.1rem; margin: 0 1rem;">{resume_status} Resume Upload</span>
                        <span style="font-size: 1.1rem; margin: 0 1rem;">{job_status} Job Description</span>
                    </div>
                    <p style="color: #718096;">Complete both uploads to enable analysis</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Disabled button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.button("🚀 Analyze Match", key="analyze_button_disabled", disabled=True)

                st.markdown("""
                <style>
                div.stButton > button:first-child:disabled {
                    background: linear-gradient(45deg, #a0aec0 0%, #cbd5e0 100%);
                    color: white;
                    padding: 1rem 3rem;
                    border: none;
                    border-radius: 50px;
                    font-size: 1.3rem;
                    font-weight: 700;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    min-width: 300px;
                    min-height: 60px;
                    margin: 0 auto;
                    display: block;
                    cursor: not-allowed;
                }
                </style>
                """, unsafe_allow_html=True)

        return False

    @staticmethod
    def render_analysis_progress():
        """Render analysis progress indicator"""
        if st.session_state.get('start_analysis', False):
            progress_bar = st.progress(0)
            status_text = st.empty()

            stages = [
                "🔄 Processing documents...",
                "🧠 Extracting skills and keywords...",
                "📊 Calculating semantic similarity...",
                "🎯 Generating match scores...",
                "💡 Creating improvement suggestions...",
                "✅ Analysis complete!"
            ]

            for i, stage in enumerate(stages):
                status_text.text(stage)
                progress_bar.progress((i + 1) / len(stages))
                time.sleep(0.5)  # Simulate processing time

            status_text.text("🎉 Analysis ready! Scroll down to see results.")
            return True
        return False

    @staticmethod
    def render_score_dashboard(score_data: Dict[str, Any]):
        """Render premium 4-column card-based dashboard"""
        st.markdown("## 📊 Match Analysis Dashboard")

        # Calculate overall score details
        overall_score = score_data["overall_score"]
        if overall_score >= 80:
            status_color = "#48bb78"
            status_text = "Excellent Match"
            status_icon = "🎉"
        elif overall_score >= 60:
            status_color = "#ed8936"
            status_text = "Good Match"
            status_icon = "✅"
        else:
            status_color = "#e53e3e"
            status_text = "Needs Improvement"
            status_icon = "🚀"

        # 4-Column Premium Card Layout
        col1, col2, col3, col4 = st.columns(4, gap="medium")

        # Card 1: Overall Score
        with col1:
            st.markdown(f"""
            <div class="premium-card">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">{status_icon}</div>
                    <div style="font-size: 2.5rem; font-weight: bold; color: {status_color}; margin-bottom: 0.5rem;">
                        {overall_score}%
                    </div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #4a5568; margin-bottom: 0.3rem;">
                        Overall Match
                    </div>
                    <div style="font-size: 0.9rem; color: {status_color}; font-weight: 500;">
                        {status_text}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Card 2: Skills Match
        skills_avg = sum(score_data["skill_matches"].values()) / len(score_data["skill_matches"]) if score_data["skill_matches"] else 0
        skills_color = "#48bb78" if skills_avg >= 70 else "#ed8936" if skills_avg >= 50 else "#e53e3e"
        with col2:
            st.markdown(f"""
            <div class="premium-card">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🛠️</div>
                    <div style="font-size: 2.5rem; font-weight: bold; color: {skills_color}; margin-bottom: 0.5rem;">
                        {skills_avg:.0f}%
                    </div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #4a5568; margin-bottom: 0.3rem;">
                        Skills Match
                    </div>
                    <div style="font-size: 0.9rem; color: {skills_color}; font-weight: 500;">
                        {"Strong" if skills_avg >= 70 else "Good" if skills_avg >= 50 else "Improving"}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Card 3: Experience Match
        exp_score = score_data['experience_match']
        exp_color = "#48bb78" if exp_score >= 70 else "#ed8936" if exp_score >= 50 else "#e53e3e"
        with col3:
            st.markdown(f"""
            <div class="premium-card">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">📅</div>
                    <div style="font-size: 2.5rem; font-weight: bold; color: {exp_color}; margin-bottom: 0.5rem;">
                        {exp_score}%
                    </div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #4a5568; margin-bottom: 0.3rem;">
                        Experience
                    </div>
                    <div style="font-size: 0.9rem; color: {exp_color}; font-weight: 500;">
                        {"Excellent" if exp_score >= 70 else "Good" if exp_score >= 50 else "Growing"}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Card 4: Semantic Similarity
        semantic_score = score_data['semantic_similarity']
        semantic_color = "#48bb78" if semantic_score >= 70 else "#ed8936" if semantic_score >= 50 else "#e53e3e"
        with col4:
            st.markdown(f"""
            <div class="premium-card">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">🧠</div>
                    <div style="font-size: 2.5rem; font-weight: bold; color: {semantic_color}; margin-bottom: 0.5rem;">
                        {semantic_score}%
                    </div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #4a5568; margin-bottom: 0.3rem;">
                        AI Alignment
                    </div>
                    <div style="font-size: 0.9rem; color: {semantic_color}; font-weight: 500;">
                        {"Excellent" if semantic_score >= 70 else "Good" if semantic_score >= 50 else "Developing"}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Secondary metrics row
        st.markdown("### 📈 Additional Metrics")
        col1, col2, col3, col4 = st.columns(4, gap="medium")

        # Skill category breakdown
        skill_categories = list(score_data["skill_matches"].items())
        for i, (category, score) in enumerate(skill_categories[:4]):  # Show up to 4 categories
            cat_color = "#48bb78" if score >= 70 else "#ed8936" if score >= 50 else "#e53e3e"
            with [col1, col2, col3, col4][i]:
                category_name = category.replace('_', ' ').title()
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: {cat_color}; font-size: 1.5rem; margin-bottom: 0.5rem;">
                        {"💻" if "programming" in category else "📊" if "data" in category else "☁️" if "cloud" in category else "🤝"}
                    </div>
                    <div class="metric-value" style="color: {cat_color};">{score}%</div>
                    <div class="metric-label">{category_name}</div>
                </div>
                """, unsafe_allow_html=True)

        # Add remaining categories if any
        if len(skill_categories) > 4:
            st.markdown("#### Other Skills")
            remaining_cols = st.columns(min(4, len(skill_categories) - 4), gap="medium")
            for i, (category, score) in enumerate(skill_categories[4:]):
                cat_color = "#48bb78" if score >= 70 else "#ed8936" if score >= 50 else "#e53e3e"
                category_name = category.replace('_', ' ').title()
                with remaining_cols[i % len(remaining_cols)]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="color: {cat_color}; font-size: 1.5rem; margin-bottom: 0.5rem;">🎯</div>
                        <div class="metric-value" style="color: {cat_color};">{score}%</div>
                        <div class="metric-label">{category_name}</div>
                    </div>
                    """, unsafe_allow_html=True)

    @staticmethod
    def render_skill_analysis(score_data: Dict[str, Any]):
        """Render enhanced skill analysis with interactive elements"""
        st.subheader("🛠️ Comprehensive Skill Analysis")

        # Skill match radar chart
        skill_categories = list(score_data["skill_matches"].keys())
        skill_scores = list(score_data["skill_matches"].values())

        # Create radar chart
        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=skill_scores,
            theta=[cat.replace('_', ' ').title() for cat in skill_categories],
            fill='toself',
            name='Your Match Score',
            line_color='#667eea'
        ))

        # Add perfect score line for reference
        fig_radar.add_trace(go.Scatterpolar(
            r=[100] * len(skill_categories),
            theta=[cat.replace('_', ' ').title() for cat in skill_categories],
            fill='toself',
            name='Perfect Score',
            line_color='rgba(255,0,0,0.3)',
            fillcolor='rgba(255,0,0,0.1)'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Skill Category Match Overview",
            height=500
        )

        st.plotly_chart(fig_radar, use_container_width=True)

        # Detailed skill breakdown with interactive tabs
        st.markdown("### 📊 Detailed Skill Breakdown")

        # Create tabs for each category
        if skill_categories:
            tabs = st.tabs([cat.replace('_', ' ').title() for cat in skill_categories])

            for i, (category, tab) in enumerate(zip(skill_categories, tabs)):
                with tab:
                    score = score_data["skill_matches"][category]
                    resume_skills = score_data["resume_skills"].get(category, [])
                    job_skills = score_data["job_skills"].get(category, [])

                    # Score indicator for this category
                    if score >= 70:
                        score_color = "🟢"
                        score_text = "Strong Match"
                    elif score >= 50:
                        score_color = "🟡"
                        score_text = "Good Match"
                    else:
                        score_color = "🔴"
                        score_text = "Needs Improvement"

                    st.markdown(f"""
                    **Category Score: {score}% {score_color} {score_text}**
                    """)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**✅ Your Skills Found:**")
                        if resume_skills:
                            for skill in resume_skills:
                                st.markdown(f"• {skill}")
                        else:
                            st.markdown("*No skills found in this category*")

                    with col2:
                        st.markdown("**🎯 Required Skills:**")
                        if job_skills:
                            for skill in job_skills:
                                # Check if skill is matched
                                if skill in resume_skills:
                                    st.markdown(f"• ✅ {skill}")
                                else:
                                    st.markdown(f"• ❌ {skill}")
                        else:
                            st.markdown("*No specific requirements in this category*")

                    # Show improvement suggestions for this category
                    missing_skills = set(job_skills) - set(resume_skills)
                    if missing_skills and len(missing_skills) <= 5:
                        st.markdown("**💡 Consider adding:**")
                        for skill in list(missing_skills)[:3]:
                            st.markdown(f"• {skill}")

        # Advanced analysis if available
        if "detailed_skill_analysis" in score_data:
            with st.expander("🔬 Advanced Skill Analysis"):
                detailed_analysis = score_data["detailed_skill_analysis"]

                for category, analysis in detailed_analysis.items():
                    if analysis.get("partial_matches"):
                        st.markdown(f"**{category.replace('_', ' ').title()} - Partial Matches:**")
                        for match in analysis["partial_matches"]:
                            confidence = match.get("score", 0) * 100
                            st.markdown(
                                f"• Your *{match['resume_skill']}* could align with required *{match['job_skill']}* "
                                f"(Confidence: {confidence:.0f}%)"
                            )

    @staticmethod
    def render_improvement_suggestions(suggestions: List[str]):
        """Render premium improvement suggestions with card-based styling"""
        st.markdown("## 💡 Personalized Improvement Suggestions")

        if not suggestions:
            st.markdown("""
            <div class="suggestion-card success">
                🎉 <strong>Excellent!</strong> Your resume is exceptionally well-matched to this position.
                You're ready to apply with confidence!
            </div>
            """, unsafe_allow_html=True)
        else:
            # Create premium card-based suggestions
            for i, suggestion in enumerate(suggestions, 1):
                # Determine card type and styling
                if suggestion.startswith("🎉"):
                    card_class = "success"
                    suggestion = suggestion.replace("🎉", "").strip()
                elif suggestion.startswith("✅"):
                    card_class = "info"
                    suggestion = suggestion.replace("✅", "").strip()
                elif suggestion.startswith("🚀"):
                    card_class = "warning"
                    suggestion = suggestion.replace("🚀", "").strip()
                else:
                    card_class = ""

                # Clean up markdown formatting for better display
                clean_suggestion = suggestion.replace("**", "").replace("*", "")

                # Extract the main action from the suggestion
                if ":" in clean_suggestion:
                    parts = clean_suggestion.split(":", 1)
                    title = parts[0].strip()
                    description = parts[1].strip()
                else:
                    title = f"Improvement {i}"
                    description = clean_suggestion

                st.markdown(f"""
                <div class="suggestion-card {card_class}">
                    <div style="display: flex; align-items: flex-start; gap: 1rem;">
                        <div style="background: rgba(102, 126, 234, 0.1); border-radius: 50%;
                                    width: 40px; height: 40px; display: flex; align-items: center;
                                    justify-content: center; font-weight: bold; color: #667eea;
                                    flex-shrink: 0;">
                            {i}
                        </div>
                        <div style="flex: 1;">
                            <div style="font-weight: 700; font-size: 1.1rem; color: #2d3748; margin-bottom: 0.5rem;">
                                {title}
                            </div>
                            <div style="color: #4a5568; line-height: 1.6;">
                                {description}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Add premium action summary
            if len(suggestions) > 1:
                action_suggestions = [s for s in suggestions if not s.startswith(("🎉", "✅"))]
                if action_suggestions:
                    st.markdown("### 🎯 Priority Action Plan")

                    st.markdown(f"""
                    <div class="premium-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                        <div style="text-align: center;">
                            <h3 style="color: white; margin-bottom: 1rem;">⚡ Quick Wins</h3>
                            <p style="color: #f7fafc; margin-bottom: 1.5rem;">
                                Focus on these high-impact areas to maximize your match score:
                            </p>
                            <div style="text-align: left; background: rgba(255,255,255,0.1);
                                        padding: 1rem; border-radius: 10px;">
                                <div style="margin-bottom: 0.5rem;">✨ <strong>Review skill gaps</strong> identified in the analysis above</div>
                                <div style="margin-bottom: 0.5rem;">🔍 <strong>Optimize keywords</strong> using terms from the job description</div>
                                <div style="margin-bottom: 0.5rem;">📈 <strong>Highlight relevant experience</strong> more prominently</div>
                                <div>🎯 <strong>Quantify achievements</strong> with specific metrics and results</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    @staticmethod
    def render_comparison_view(score_data: Dict[str, Any]):
        """Render premium comparison view with consistent styling"""
        st.markdown("## 📈 Score Improvement Potential")

        current_score = score_data["overall_score"]

        # Calculate potential score more conservatively
        potential_improvements = {
            "Adding missing skills": 12,
            "Keyword optimization": 6,
            "Experience highlighting": 8,
            "Language alignment": 7
        }

        max_potential = min(100, current_score + sum(potential_improvements.values()) * 0.5)

        # Premium comparison cards
        col1, col2, col3 = st.columns([1, 1, 1], gap="large")

        # Current Score Card
        with col1:
            current_color = "#48bb78" if current_score >= 70 else "#ed8936" if current_score >= 50 else "#e53e3e"
            st.markdown(f"""
            <div class="premium-card">
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
                    <div style="font-size: 2rem; font-weight: bold; color: {current_color}; margin-bottom: 0.5rem;">
                        {current_score:.1f}%
                    </div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #4a5568;">
                        Current Score
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Potential Score Card
        with col2:
            potential_color = "#48bb78" if max_potential >= 70 else "#ed8936"
            st.markdown(f"""
            <div class="premium-card">
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎯</div>
                    <div style="font-size: 2rem; font-weight: bold; color: {potential_color}; margin-bottom: 0.5rem;">
                        {max_potential:.1f}%
                    </div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #4a5568;">
                        Potential Score
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Improvement Potential Card
        with col3:
            improvement = max_potential - current_score
            st.markdown(f"""
            <div class="premium-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem; color: white;">🚀</div>
                    <div style="font-size: 2rem; font-weight: bold; color: white; margin-bottom: 0.5rem;">
                        +{improvement:.1f}%
                    </div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #f7fafc;">
                        Growth Potential
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Improvement roadmap
        if improvement > 5:
            st.markdown("### 🛣️ Improvement Roadmap")
            st.markdown(f"""
            <div class="premium-card">
                <h4 style="color: #4a5568; margin-bottom: 1rem;">📋 Strategic Improvements</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                    <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px;">
                        <strong style="color: #667eea;">🎯 Skills Enhancement</strong>
                        <p style="color: #4a5568; margin: 0.5rem 0 0 0;">Focus on adding 2-3 key missing skills for maximum impact</p>
                    </div>
                    <div style="background: rgba(237, 137, 54, 0.1); padding: 1rem; border-radius: 10px;">
                        <strong style="color: #ed8936;">🔍 Keyword Optimization</strong>
                        <p style="color: #4a5568; margin: 0.5rem 0 0 0;">Integrate job-specific terminology throughout your resume</p>
                    </div>
                    <div style="background: rgba(72, 187, 120, 0.1); padding: 1rem; border-radius: 10px;">
                        <strong style="color: #48bb78;">📈 Experience Highlighting</strong>
                        <p style="color: #4a5568; margin: 0.5rem 0 0 0;">Emphasize transferable skills and relevant achievements</p>
                    </div>
                    <div style="background: rgba(66, 153, 225, 0.1); padding: 1rem; border-radius: 10px;">
                        <strong style="color: #4299e1;">💬 Language Alignment</strong>
                        <p style="color: #4a5568; margin: 0.5rem 0 0 0;">Match the tone and terminology used in the job posting</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

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