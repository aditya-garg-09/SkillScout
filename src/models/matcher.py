import re
import numpy as np
from typing import Dict, List, Tuple, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st


class ResumeJobMatcher:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.skill_keywords = self._load_skill_keywords()

    def _load_skill_keywords(self) -> Dict[str, List[str]]:
        """Load common skill keywords by category"""
        return {
            "programming": [
                "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
                "react", "angular", "vue", "node.js", "django", "flask", "spring"
            ],
            "data_science": [
                "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
                "pandas", "numpy", "sql", "nosql", "mongodb", "postgresql"
            ],
            "cloud": [
                "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
                "jenkins", "ci/cd", "devops"
            ],
            "soft_skills": [
                "leadership", "communication", "teamwork", "problem solving",
                "project management", "agile", "scrum"
            ]
        }

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills from text by category"""
        text_lower = text.lower()
        found_skills = {}

        for category, skills in self.skill_keywords.items():
            found_skills[category] = []
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills[category].append(skill)

        return found_skills

    def calculate_skill_match(self, resume_skills: Dict[str, List[str]],
                            job_skills: Dict[str, List[str]]) -> Dict[str, float]:
        """Calculate skill match percentage by category"""
        match_scores = {}

        for category in self.skill_keywords.keys():
            resume_category_skills = set(resume_skills.get(category, []))
            job_category_skills = set(job_skills.get(category, []))

            if not job_category_skills:
                match_scores[category] = 0.0
            else:
                intersection = resume_category_skills.intersection(job_category_skills)
                match_scores[category] = len(intersection) / len(job_category_skills)

        return match_scores

    def extract_experience_years(self, text: str) -> int:
        """Extract years of experience from text"""
        patterns = [
            r'(\d+)\s*years?\s*of\s*experience',
            r'(\d+)\s*years?\s*experience',
            r'(\d+)\+\s*years?',
            r'over\s*(\d+)\s*years?'
        ]

        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return int(match.group(1))

        return 0

    def calculate_experience_match(self, resume_text: str, job_text: str) -> float:
        """Calculate experience level match"""
        resume_years = self.extract_experience_years(resume_text)
        job_years = self.extract_experience_years(job_text)

        if job_years == 0:
            return 1.0  # No specific requirement

        if resume_years >= job_years:
            return 1.0
        else:
            return resume_years / job_years

    def calculate_semantic_similarity(self, resume_text: str, job_text: str) -> float:
        """Calculate semantic similarity using embeddings"""
        return self.embedding_model.compute_similarity(resume_text, job_text)

    def calculate_keyword_density(self, resume_text: str, job_text: str) -> float:
        """Calculate keyword overlap using TF-IDF"""
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception:
            return 0.0

    def generate_comprehensive_score(self, resume_text: str, job_text: str) -> Dict[str, Any]:
        """Generate comprehensive matching score"""
        # Extract skills
        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_text)

        # Calculate various match scores
        skill_matches = self.calculate_skill_match(resume_skills, job_skills)
        experience_match = self.calculate_experience_match(resume_text, job_text)
        semantic_similarity = self.calculate_semantic_similarity(resume_text, job_text)
        keyword_density = self.calculate_keyword_density(resume_text, job_text)

        # Calculate weighted overall score
        overall_score = (
            np.mean(list(skill_matches.values())) * 0.4 +
            experience_match * 0.2 +
            semantic_similarity * 0.25 +
            keyword_density * 0.15
        )

        return {
            "overall_score": round(overall_score * 100, 2),
            "skill_matches": {k: round(v * 100, 2) for k, v in skill_matches.items()},
            "experience_match": round(experience_match * 100, 2),
            "semantic_similarity": round(semantic_similarity * 100, 2),
            "keyword_density": round(keyword_density * 100, 2),
            "resume_skills": resume_skills,
            "job_skills": job_skills
        }

    def generate_improvement_suggestions(self, score_data: Dict[str, Any]) -> List[str]:
        """Generate suggestions for improving resume match"""
        suggestions = []

        # Check skill gaps
        for category, score in score_data["skill_matches"].items():
            if score < 50:
                missing_skills = set(score_data["job_skills"][category]) - set(score_data["resume_skills"][category])
                if missing_skills:
                    suggestions.append(
                        f"Consider adding {category} skills: {', '.join(list(missing_skills)[:3])}"
                    )

        # Check experience
        if score_data["experience_match"] < 70:
            suggestions.append("Highlight relevant experience more prominently or consider emphasizing transferable skills")

        # Check keyword optimization
        if score_data["keyword_density"] < 40:
            suggestions.append("Include more keywords from the job description to improve ATS compatibility")

        # Check semantic similarity
        if score_data["semantic_similarity"] < 60:
            suggestions.append("Align your resume language more closely with the job description terminology")

        return suggestions