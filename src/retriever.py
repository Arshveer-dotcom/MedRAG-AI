from typing import List, Dict, Any
from .vector_store import MedicalVectorStore
from .embeddings import MedicalEmbeddings

class MedicalRetriever:
    """Handles semantic retrieval of medical information."""
    
    def __init__(self, vector_store: MedicalVectorStore, embeddings: MedicalEmbeddings):
        self.vector_store = vector_store
        self.embeddings = embeddings
    
    def retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        print(f"Retrieving relevant chunks for query: '{query[:50]}...'")
        
        results = self.vector_store.similarity_search(query, k=top_k)
        
        print(f"Retrieved {len(results)} relevant chunks")
        return results
    
    def format_context_for_llm(self, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return "No relevant information found in the medical knowledge base."
        
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            metadata = chunk['metadata']
            content = chunk['content']
            
            context_part = f"""
Source {i}: {metadata['document_name']} (Page {metadata['page_number']})
Content: {content}
"""
            context_parts.append(context_part)
        
        return "\n".join(context_parts)