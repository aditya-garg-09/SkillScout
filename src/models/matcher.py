import re
import numpy as np
from typing import Dict, List, Tuple, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher
import streamlit as st


class ResumeJobMatcher:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.skill_keywords = self._load_skill_keywords()

    def _load_skill_keywords(self) -> Dict[str, Dict[str, Any]]:
        """Load enhanced skill keywords with synonyms, weights, and categories"""
        return {
            "programming": {
                "weight": 0.4,  # Higher weight for technical roles
                "skills": {
                    "python": {"synonyms": ["py", "python3"], "level": "core"},
                    "java": {"synonyms": ["java8", "java11", "openjdk"], "level": "core"},
                    "javascript": {"synonyms": ["js", "ecmascript", "es6", "es2020"], "level": "core"},
                    "typescript": {"synonyms": ["ts"], "level": "advanced"},
                    "c++": {"synonyms": ["cpp", "c plus plus"], "level": "core"},
                    "c#": {"synonyms": ["csharp", "c sharp", ".net"], "level": "core"},
                    "go": {"synonyms": ["golang"], "level": "advanced"},
                    "rust": {"synonyms": [], "level": "advanced"},
                    "react": {"synonyms": ["reactjs", "react.js"], "level": "framework"},
                    "angular": {"synonyms": ["angularjs", "angular2+"], "level": "framework"},
                    "vue": {"synonyms": ["vuejs", "vue.js"], "level": "framework"},
                    "node.js": {"synonyms": ["nodejs", "node js"], "level": "framework"},
                    "django": {"synonyms": [], "level": "framework"},
                    "flask": {"synonyms": [], "level": "framework"},
                    "spring": {"synonyms": ["spring boot", "spring framework"], "level": "framework"}
                }
            },
            "data_science": {
                "weight": 0.35,
                "skills": {
                    "machine learning": {"synonyms": ["ml", "artificial intelligence", "ai"], "level": "core"},
                    "deep learning": {"synonyms": ["dl", "neural networks"], "level": "advanced"},
                    "tensorflow": {"synonyms": ["tf"], "level": "framework"},
                    "pytorch": {"synonyms": [], "level": "framework"},
                    "scikit-learn": {"synonyms": ["sklearn", "scikit learn"], "level": "framework"},
                    "pandas": {"synonyms": [], "level": "core"},
                    "numpy": {"synonyms": [], "level": "core"},
                    "sql": {"synonyms": ["mysql", "postgresql", "sqlite"], "level": "core"},
                    "nosql": {"synonyms": ["mongodb", "cassandra", "redis"], "level": "advanced"},
                    "mongodb": {"synonyms": ["mongo"], "level": "framework"},
                    "postgresql": {"synonyms": ["postgres"], "level": "framework"}
                }
            },
            "cloud": {
                "weight": 0.3,
                "skills": {
                    "aws": {"synonyms": ["amazon web services"], "level": "core"},
                    "azure": {"synonyms": ["microsoft azure"], "level": "core"},
                    "gcp": {"synonyms": ["google cloud", "google cloud platform"], "level": "core"},
                    "docker": {"synonyms": ["containerization"], "level": "core"},
                    "kubernetes": {"synonyms": ["k8s"], "level": "advanced"},
                    "terraform": {"synonyms": ["iac", "infrastructure as code"], "level": "advanced"},
                    "jenkins": {"synonyms": [], "level": "framework"},
                    "ci/cd": {"synonyms": ["continuous integration", "continuous deployment"], "level": "advanced"},
                    "devops": {"synonyms": [], "level": "methodology"}
                }
            },
            "soft_skills": {
                "weight": 0.2,
                "skills": {
                    "leadership": {"synonyms": ["team lead", "management"], "level": "advanced"},
                    "communication": {"synonyms": ["collaboration"], "level": "core"},
                    "teamwork": {"synonyms": ["team player", "collaboration"], "level": "core"},
                    "problem solving": {"synonyms": ["analytical thinking", "troubleshooting"], "level": "core"},
                    "project management": {"synonyms": ["pm"], "level": "advanced"},
                    "agile": {"synonyms": ["scrum", "kanban"], "level": "methodology"},
                    "scrum": {"synonyms": ["agile"], "level": "methodology"}
                }
            }
        }

    def _fuzzy_match(self, skill1: str, skill2: str, threshold: float = 0.8) -> float:
        """Calculate fuzzy matching score between two skills"""
        return SequenceMatcher(None, skill1.lower(), skill2.lower()).ratio()

    def _find_skill_with_synonyms(self, target_skill: str, text: str, synonyms: List[str]) -> Tuple[bool, float]:
        """Find skill in text considering synonyms and fuzzy matching"""
        text_lower = text.lower()
        target_lower = target_skill.lower()

        # Direct match
        if target_lower in text_lower:
            return True, 1.0

        # Synonym match
        for synonym in synonyms:
            if synonym.lower() in text_lower:
                return True, 0.95  # Slight penalty for synonym match

        # Fuzzy match with more liberal threshold
        words = text_lower.split()
        for word in words:
            fuzzy_score = self._fuzzy_match(target_lower, word, 0.75)
            if fuzzy_score >= 0.75:
                # Progressive confidence based on fuzzy score
                confidence = 0.6 + (fuzzy_score - 0.75) * 0.8  # Scale from 0.6 to 1.0
                return True, confidence

        return False, 0.0

    def extract_skills(self, text: str) -> Dict[str, Dict[str, float]]:
        """Extract skills from text with confidence scores"""
        found_skills = {}

        for category, category_data in self.skill_keywords.items():
            found_skills[category] = {}
            skills_data = category_data["skills"]

            for skill, skill_info in skills_data.items():
                found, confidence = self._find_skill_with_synonyms(
                    skill, text, skill_info["synonyms"]
                )
                if found:
                    found_skills[category][skill] = confidence

        return found_skills

    def calculate_advanced_skill_match(self, resume_skills: Dict[str, Dict[str, float]],
                                     job_skills: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Calculate comprehensive skill match with partial credit and weighting"""
        match_data = {}

        for category, category_data in self.skill_keywords.items():
            category_weight = category_data["weight"]
            resume_category = resume_skills.get(category, {})
            job_category = job_skills.get(category, {})

            if not job_category:
                match_data[category] = {
                    "score": 1.0,  # No requirements means perfect match
                    "matched_skills": [],
                    "missing_skills": [],
                    "partial_matches": []
                }
                continue

            total_required = len(job_category)
            matched_skills = []
            missing_skills = []
            partial_matches = []
            total_score = 0.0

            for job_skill, job_confidence in job_category.items():
                if job_skill in resume_category:
                    # Direct match
                    resume_confidence = resume_category[job_skill]
                    skill_score = min(job_confidence, resume_confidence)
                    matched_skills.append({
                        "skill": job_skill,
                        "score": skill_score,
                        "type": "exact"
                    })
                    total_score += skill_score
                else:
                    # Look for partial matches (similar skills)
                    best_partial_match = 0.0
                    best_match_skill = None

                    for resume_skill, resume_confidence in resume_category.items():
                        similarity = self._fuzzy_match(job_skill, resume_skill)
                        if similarity >= 0.7:
                            partial_score = similarity * resume_confidence * 0.7  # Penalty for partial match
                            if partial_score > best_partial_match:
                                best_partial_match = partial_score
                                best_match_skill = resume_skill

                    if best_partial_match > 0:
                        partial_matches.append({
                            "job_skill": job_skill,
                            "resume_skill": best_match_skill,
                            "score": best_partial_match,
                            "type": "partial"
                        })
                        total_score += best_partial_match
                    else:
                        missing_skills.append(job_skill)

            # Enhanced liberal scoring calculation
            base_score = total_score / total_required if total_required > 0 else 1.0

            # More generous bonus system
            extra_skills = len(resume_category) - len(matched_skills) - len(partial_matches)
            skill_bonus = min(0.15, extra_skills * 0.03)  # Max 15% bonus for extra skills

            # Coverage bonus: Reward for having some skills even if not all
            coverage_ratio = (len(matched_skills) + len(partial_matches)) / total_required if total_required > 0 else 1.0
            coverage_bonus = min(0.1, coverage_ratio * 0.1)  # Up to 10% bonus for good coverage

            # Liberal adjustment: Reduce penalty for missing skills
            if base_score < 0.7 and len(matched_skills) > 0:
                # Give credit for having ANY relevant skills
                liberal_adjustment = min(0.2, len(matched_skills) * 0.05)  # Up to 20% boost
                base_score = min(1.0, base_score + liberal_adjustment)

            final_score = min(1.0, base_score + skill_bonus + coverage_bonus)

            match_data[category] = {
                "score": final_score,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "partial_matches": partial_matches,
                "weight": category_weight
            }

        return match_data

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
        """Calculate liberal experience level match"""
        resume_years = self.extract_experience_years(resume_text)
        job_years = self.extract_experience_years(job_text)

        if job_years == 0:
            return 1.0  # No specific requirement

        if resume_years >= job_years:
            return 1.0
        else:
            # More liberal experience matching
            ratio = resume_years / job_years

            # Give significant credit for having some experience
            if resume_years > 0:
                # Liberal adjustment: reduce experience gap penalty
                liberal_ratio = ratio + (1 - ratio) * 0.4  # Close 40% of the gap

                # Additional boost for candidates with reasonable experience
                if ratio >= 0.6:  # 60% of required experience
                    liberal_ratio = min(1.0, liberal_ratio + 0.1)  # 10% bonus
                elif ratio >= 0.4:  # 40% of required experience
                    liberal_ratio = min(1.0, liberal_ratio + 0.05)  # 5% bonus

                return liberal_ratio
            else:
                # Even no explicit experience gets some credit if other factors are strong
                return 0.3  # 30% base score instead of 0

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
        """Generate comprehensive matching score with advanced algorithm"""
        # Extract skills with confidence scores
        resume_skills = self.extract_skills(resume_text)
        job_skills = self.extract_skills(job_text)

        # Calculate advanced skill matching
        skill_match_data = self.calculate_advanced_skill_match(resume_skills, job_skills)

        # Calculate other match scores
        experience_match = self.calculate_experience_match(resume_text, job_text)
        semantic_similarity = self.calculate_semantic_similarity(resume_text, job_text)
        keyword_density = self.calculate_keyword_density(resume_text, job_text)

        # Calculate weighted skill score
        weighted_skill_score = 0.0
        total_weight = 0.0
        simple_skill_scores = {}

        for category, match_info in skill_match_data.items():
            weight = match_info["weight"]
            score = match_info["score"]
            weighted_skill_score += score * weight
            total_weight += weight
            simple_skill_scores[category] = score

        # Normalize skill score
        final_skill_score = weighted_skill_score / total_weight if total_weight > 0 else 0.0

        # Calculate enhanced overall score with liberal adjustments
        base_overall = (
            final_skill_score * 0.40 +      # Balanced skill weight
            experience_match * 0.25 +       # Increased experience weight
            semantic_similarity * 0.25 +    # Semantic similarity
            keyword_density * 0.10          # Keyword density
        )

        # Liberal overall score adjustments
        if base_overall >= 0.6:
            # Good candidates get a boost
            liberal_boost = min(0.15, (base_overall - 0.6) * 0.3)
            overall_score = min(1.0, base_overall + liberal_boost)
        elif base_overall >= 0.4:
            # Give moderate candidates a fair chance
            liberal_boost = min(0.1, (final_skill_score + semantic_similarity) / 2 * 0.2)
            overall_score = min(1.0, base_overall + liberal_boost)
        else:
            # Even lower scores get some consideration if they have potential
            if final_skill_score > 0.3 or semantic_similarity > 0.5:
                liberal_boost = min(0.08, max(final_skill_score, semantic_similarity) * 0.15)
                overall_score = min(1.0, base_overall + liberal_boost)
            else:
                overall_score = base_overall

        # Convert skills back to simple format for UI compatibility
        resume_skills_simple = {}
        job_skills_simple = {}

        for category in self.skill_keywords.keys():
            resume_skills_simple[category] = list(resume_skills.get(category, {}).keys())
            job_skills_simple[category] = list(job_skills.get(category, {}).keys())

        return {
            "overall_score": round(overall_score * 100, 2),
            "skill_matches": {k: round(v * 100, 2) for k, v in simple_skill_scores.items()},
            "experience_match": round(experience_match * 100, 2),
            "semantic_similarity": round(semantic_similarity * 100, 2),
            "keyword_density": round(keyword_density * 100, 2),
            "resume_skills": resume_skills_simple,
            "job_skills": job_skills_simple,
            "detailed_skill_analysis": skill_match_data  # Advanced analysis for detailed view
        }

    def generate_improvement_suggestions(self, score_data: Dict[str, Any]) -> List[str]:
        """Generate intelligent suggestions based on advanced scoring"""
        suggestions = []

        # Analyze detailed skill data
        detailed_analysis = score_data.get("detailed_skill_analysis", {})

        for category, analysis in detailed_analysis.items():
            category_score = analysis["score"] * 100
            missing_skills = analysis["missing_skills"]
            partial_matches = analysis["partial_matches"]

            # Suggest missing critical skills
            if category_score < 70 and missing_skills:
                skill_count = min(3, len(missing_skills))
                suggestions.append(
                    f"🎯 **{category.replace('_', ' ').title()}**: Add {', '.join(missing_skills[:skill_count])} "
                    f"to improve your {category.replace('_', ' ')} match"
                )

            # Highlight partial matches that could be strengthened
            if partial_matches:
                for match in partial_matches[:2]:  # Top 2 partial matches
                    suggestions.append(
                        f"📈 **Strengthen Skills**: Your {match['resume_skill']} experience could align better with "
                        f"required {match['job_skill']} - consider highlighting relevant projects"
                    )

        # Experience analysis
        if score_data["experience_match"] < 70:
            suggestions.append(
                "📅 **Experience**: Emphasize relevant experience more prominently or highlight transferable skills "
                "that demonstrate your capability in this role"
            )

        # Keyword optimization
        if score_data["keyword_density"] < 30:
            suggestions.append(
                "🔍 **ATS Optimization**: Include more specific keywords from the job description to improve "
                "Applicant Tracking System compatibility"
            )

        # Semantic alignment
        if score_data["semantic_similarity"] < 60:
            suggestions.append(
                "💬 **Language Alignment**: Use terminology and phrases from the job description to better "
                "demonstrate your fit for this specific role"
            )

        # Overall score guidance
        overall_score = score_data["overall_score"]
        if overall_score >= 80:
            suggestions.insert(0, "🎉 **Excellent Match!** Your resume aligns very well with this position. Consider applying with confidence!")
        elif overall_score >= 60:
            suggestions.insert(0, "✅ **Good Match**: You're a strong candidate! Focus on the suggestions below to strengthen your application.")
        else:
            suggestions.insert(0, "🚀 **Growth Opportunity**: With some targeted improvements, you can significantly increase your match score.")

        return suggestions[:6]  # Limit to 6 most important suggestions