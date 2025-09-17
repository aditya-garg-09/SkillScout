import streamlit as st
import numpy as np
from typing import List, Dict, Tuple
import hashlib
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingModel:
    def __init__(self, model_name: str = "tfidf"):
        self.model_name = model_name
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        self.storage_file = "document_storage.pkl"
        self.documents = {}
        self.fitted = False

    def load_model(self):
        """Initialize the TF-IDF vectorizer"""
        return self.vectorizer


    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate TF-IDF embeddings for a list of texts"""
        try:
            if not self.fitted:
                # Fit on the provided texts
                self.vectorizer.fit(texts)
                self.fitted = True

            embeddings = self.vectorizer.transform(texts).toarray()
            return embeddings
        except Exception as e:
            st.error(f"Error generating embeddings: {str(e)}")
            return np.array([])

    def store_document(self, text: str, metadata: Dict, doc_type: str = "resume"):
        """Store document in simple file storage"""
        doc_id = hashlib.md5(text.encode()).hexdigest()

        # Load existing documents
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'rb') as f:
                    self.documents = pickle.load(f)
            except:
                self.documents = {}

        # Store new document
        embedding = self.generate_embeddings([text])
        self.documents[doc_id] = {
            'text': text,
            'metadata': {**metadata, "type": doc_type},
            'embedding': embedding[0].tolist() if len(embedding) > 0 else []
        }

        # Save to file
        try:
            with open(self.storage_file, 'wb') as f:
                pickle.dump(self.documents, f)
            return doc_id
        except Exception as e:
            st.error(f"Error storing document: {str(e)}")
            return None

    def search_similar(self, query_text: str, n_results: int = 5) -> List[Dict]:
        """Search for similar documents"""
        query_embedding = self.generate_embeddings([query_text])
        if len(query_embedding) == 0:
            return []

        query_embedding = query_embedding[0]
        similar_docs = []

        # Load documents
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'rb') as f:
                    self.documents = pickle.load(f)
            except:
                return []

        # Calculate similarities
        for doc_id, doc_data in self.documents.items():
            if doc_data['embedding']:
                doc_embedding = np.array(doc_data['embedding'])
                similarity = np.dot(query_embedding, doc_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
                )

                similar_docs.append({
                    'id': doc_id,
                    'document': doc_data['text'],
                    'metadata': doc_data['metadata'],
                    'distance': 1 - similarity
                })

        # Sort by similarity
        similar_docs.sort(key=lambda x: x['distance'])
        return similar_docs[:n_results]

    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity between two texts"""
        try:
            embeddings = self.generate_embeddings([text1, text2])
            if len(embeddings) < 2:
                return 0.0

            # Use sklearn's cosine_similarity for better handling
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return float(similarity)
        except Exception as e:
            st.error(f"Error computing similarity: {str(e)}")
            return 0.0