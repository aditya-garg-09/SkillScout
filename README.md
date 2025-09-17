# 🎯 AI Resume Analyzer & Job Matcher

An intelligent resume analysis tool that uses NLP and RAG (Retrieval-Augmented Generation) to match resumes with job descriptions, providing detailed scoring and improvement suggestions.

## ✨ Features

- **Document Processing**: Supports PDF, DOCX, and TXT file formats
- **Semantic Analysis**: Uses sentence transformers for deep semantic understanding
- **Skill Extraction**: Automatically identifies and categorizes technical and soft skills
- **Match Scoring**: Comprehensive scoring algorithm with multiple factors
- **Improvement Suggestions**: AI-powered recommendations for resume optimization
- **Vector Database**: ChromaDB integration for document storage and retrieval
- **Interactive Dashboard**: Beautiful Streamlit interface with visualizations

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **NLP**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB
- **ML**: scikit-learn, numpy, pandas
- **Visualization**: Plotly
- **Document Processing**: PyPDF2, python-docx

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd KitLab
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 🚀 Usage

1. **Upload Resume**: Upload your resume in PDF, DOCX, or TXT format
2. **Provide Job Description**: Either upload a file or paste the job description text
3. **Get Analysis**: View comprehensive matching analysis including:
   - Overall match score
   - Skill-by-skill breakdown
   - Experience level matching
   - Semantic similarity analysis
   - Keyword density optimization
4. **Follow Suggestions**: Implement AI-generated improvement recommendations

## 📊 Scoring Algorithm

The matching score is calculated using a weighted combination of:

- **Skill Matching (40%)**: Category-wise skill alignment
- **Semantic Similarity (25%)**: Deep semantic understanding using embeddings
- **Experience Match (20%)**: Years of experience comparison
- **Keyword Density (15%)**: Resume-job description keyword overlap

## 🎯 Score Interpretation

- **90-100%**: Excellent match - Strong candidate
- **70-89%**: Good match - Qualified candidate
- **50-69%**: Fair match - Some adjustments needed
- **Below 50%**: Needs improvement - Significant gaps identified

## 📁 Project Structure

```
KitLab/
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   └── ui_components.py     # Streamlit UI components
│   ├── models/
│   │   ├── __init__.py
│   │   ├── embeddings.py        # Embedding model and vector DB
│   │   └── matcher.py           # Resume-job matching logic
│   ├── utils/
│   │   ├── __init__.py
│   │   └── document_parser.py   # Document processing utilities
│   └── __init__.py
├── data/
│   ├── resumes/                 # Sample resumes
│   └── job_descriptions/        # Sample job descriptions
├── chroma_db/                   # Vector database storage
├── app.py                       # Main Streamlit application
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔧 Configuration

The application uses default configurations that work well out of the box:

- **Embedding Model**: `all-MiniLM-L6-v2` (lightweight and efficient)
- **Vector Database**: ChromaDB with DuckDB backend
- **Similarity Threshold**: Configurable in the matcher module

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Sentence Transformers for the embedding models
- ChromaDB for vector database capabilities
- Streamlit for the amazing web framework
- The open-source community for the various libraries used

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

**Happy job hunting! 🎉**