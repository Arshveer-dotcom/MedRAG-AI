from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List, Dict, Any, Optional
from pathlib import Path

class MedicalVectorStore:
    """Handles ChromaDB vector store operations."""
    
    def __init__(self, persist_directory: Path, collection_name: str = "medical_documents"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        persist_directory.mkdir(parents=True, exist_ok=True)
        
        self.vector_store = Chroma(
            collection_name=collection_name,
            persist_directory=str(persist_directory)
        )
        
        print(f"Initialized ChromaDB vector store at: {persist_directory}")
        print(f"Collection: {collection_name}")
    
    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]) -> int:
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks must match number of embeddings")
        
        documents = []
        metadatas = []
        ids = []
        
        for chunk, embedding in zip(chunks, embeddings):
            doc = Document(
                page_content=chunk['text'],
                metadata={
                    'document_name': chunk['document_name'],
                    'page_number': chunk['page_number'],
                    'chunk_id': chunk['chunk_id'],
                    'chunk_number': chunk['chunk_number'],
                    'document_path': chunk['document_path'],
                    'total_pages': chunk['total_pages']
                }
            )
            documents.append(doc)
            metadatas.append(doc.metadata)
            ids.append(chunk['chunk_id'])
        
        self.vector_store.add_documents(
            documents=documents,
            embeddings=embeddings,
            ids=ids
        )
        
        print(f"Added {len(documents)} documents to vector store")
        return len(documents)
    
    def get_retriever(self, search_k: int = 5):
        return self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": search_k}
        )
    
    def similarity_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                'content': doc.page_content,
                'metadata': doc.metadata,
                'score': float(score)
            })
        
        return formatted_results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        collection = self.vector_store._collection
        return {
            'collection_name': self.collection_name,
            'document_count': collection.count(),
            'persist_directory': str(self.persist_directory)
        }