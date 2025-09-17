import PyPDF2
import docx
import streamlit as st
from typing import List, Dict, Any
import re


class DocumentParser:
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> str:
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""

    @staticmethod
    def extract_text_from_docx(docx_file) -> str:
        try:
            doc = docx.Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""

    @staticmethod
    def extract_text_from_txt(txt_file) -> str:
        try:
            return txt_file.read().decode('utf-8').strip()
        except Exception as e:
            st.error(f"Error reading TXT: {str(e)}")
            return ""

    @classmethod
    def parse_document(cls, uploaded_file) -> str:
        if uploaded_file is None:
            return ""

        file_type = uploaded_file.type

        if file_type == "application/pdf":
            return cls.extract_text_from_pdf(uploaded_file)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return cls.extract_text_from_docx(uploaded_file)
        elif file_type == "text/plain":
            return cls.extract_text_from_txt(uploaded_file)
        else:
            st.error(f"Unsupported file type: {file_type}")
            return ""

    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
        return text.strip()

    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        sections = {
            'contact': '',
            'summary': '',
            'experience': '',
            'education': '',
            'skills': '',
            'other': ''
        }

        text_lower = text.lower()

        # Simple section detection
        if 'summary' in text_lower or 'objective' in text_lower:
            sections['summary'] = text[:200]  # First 200 chars as summary

        if 'experience' in text_lower or 'work' in text_lower:
            sections['experience'] = text

        if 'education' in text_lower or 'degree' in text_lower:
            sections['education'] = text

        if 'skills' in text_lower or 'technologies' in text_lower:
            sections['skills'] = text

        sections['other'] = text

        return sections