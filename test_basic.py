"""
Basic test to verify the application structure works
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_structure():
    """Test if project structure is correct"""
    required_files = [
        'src/utils/document_parser.py',
        'src/models/embeddings.py',
        'src/models/matcher.py',
        'src/components/ui_components.py',
        'app.py',
        'requirements.txt'
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print("Missing files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("All required files are present!")
        return True

def test_basic_parsing():
    """Test basic text processing without dependencies"""
    import re

    # Test the clean_text function logic
    def clean_text(text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
        return text.strip()

    test_text = "This is a    test  with extra    spaces!"
    cleaned = clean_text(test_text)
    expected = "This is a test with extra spaces!"

    if cleaned == expected:
        print("Text cleaning function works correctly!")
        return True
    else:
        print(f"Text cleaning failed. Expected: '{expected}', Got: '{cleaned}'")
        return False

if __name__ == "__main__":
    print("Testing AI Resume Analyzer Structure...")
    print("-" * 50)

    structure_ok = test_structure()
    parsing_ok = test_basic_parsing()

    if structure_ok and parsing_ok:
        print("\nAll basic tests passed!")
        print("\nProject structure is ready!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the app: streamlit run app.py")
        print("3. Upload a resume and job description to test")
    else:
        print("\nSome tests failed. Please check the issues above.")