from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class MedicalEmbeddings:
    """Handles embedding generation for medical documents."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        print(f"Loading embedding model: {model_name}")
        
        try:
            self.model = SentenceTransformer(model_name)
            print(f"Successfully loaded model: {model_name}")
        except Exception as e:
            print(f"Error loading model {model_name}: {str(e)}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        
        print(f"Generating embeddings for {len(texts)} texts...")
        
        try:
            embeddings = self.model.encode(texts, show_progress_bar=True)
            print(f"Successfully generated {len(embeddings)} embeddings")
            return embeddings.tolist()
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            raise
    
    def generate_single_embedding(self, text: str) -> List[float]:
        return self.generate_embeddings([text])[0]