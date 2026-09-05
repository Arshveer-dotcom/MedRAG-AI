from typing import Dict, Any, List
from pathlib import Path
from .config import OLLAMA_BASE_URL, OLLAMA_MODEL, EMBEDDING_MODEL_NAME, CHROMA_PERSIST_DIRECTORY, CHROMA_COLLECTION_NAME, TOP_K_RETRIEVAL, MAX_CHUNK_SIZE, CHUNK_OVERLAP, OPENAI_API_KEY, OPENAI_MODEL
from .embeddings import MedicalEmbeddings
from .vector_store import MedicalVectorStore
from .retriever import MedicalRetriever
from .llm import MedicalLLM
from .pdf_processor import PDFProcessor
from .text_splitter import MedicalTextSplitter

class MedicalRAGPipeline:
    """Complete RAG pipeline for medical information retrieval."""
    
    def __init__(self):
        print("Initializing Medical RAG Pipeline...")
        
        self.embeddings = MedicalEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        
        self.vector_store = MedicalVectorStore(
            persist_directory=CHROMA_PERSIST_DIRECTORY,
            collection_name=CHROMA_COLLECTION_NAME
        )
        
        self.retriever = MedicalRetriever(
            vector_store=self.vector_store,
            embeddings=self.embeddings
        )
        
        self.llm = MedicalLLM(
            model_name=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            openai_api_key=OPENAI_API_KEY,
            openai_model=OPENAI_MODEL,
        )
        
        self.text_splitter = MedicalTextSplitter(
            chunk_size=MAX_CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        
        print("Medical RAG Pipeline initialized successfully")
    
    def ingest_documents(self, docs_dir: Path) -> int:
        print(f"Ingesting documents from: {docs_dir}")
        
        pages = PDFProcessor.process_medical_documents(docs_dir)
        
        if not pages:
            print("No pages extracted from documents")
            return 0
        
        chunks = self.text_splitter.split_pages_into_chunks(pages)
        
        if not chunks:
            print("No chunks created from extracted pages")
            return 0
        
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.embeddings.generate_embeddings(texts)
        
        num_added = self.vector_store.add_chunks(chunks, embeddings)
        
        print(f"Successfully ingested {num_added} chunks into vector store")
        return num_added
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        print(f"\nProcessing question: '{question[:50]}...'")
        
        relevant_chunks = self.retriever.retrieve_relevant_chunks(
            question, 
            top_k=TOP_K_RETRIEVAL
        )
        
        if not relevant_chunks:
            return {
                'answer': "I could not find this information in the available medical knowledge base.",
                'sources': [],
                'context_used': False,
                'question': question
            }
        
        context = self.retriever.format_context_for_llm(relevant_chunks)
        
        answer = self.llm.generate_medical_answer(context, question)
        
        sources = []
        for chunk in relevant_chunks:
            metadata = chunk['metadata']
            sources.append({
                'document_name': metadata['document_name'],
                'page_number': metadata['page_number'],
                'chunk_id': metadata['chunk_id'],
                'relevance_score': chunk['score']
            })
        
        result = {
            'answer': answer,
            'sources': sources,
            'context_used': True,
            'question': question,
            'num_chunks_retrieved': len(relevant_chunks)
        }
        
        print(f"Generated answer with {len(sources)} sources")
        return result
    
    def get_pipeline_info(self) -> Dict[str, Any]:
        vector_store_stats = self.vector_store.get_collection_stats()
        
        return {
            'embedding_model': EMBEDDING_MODEL_NAME,
            'llm_model': OLLAMA_MODEL,
            'vector_store': vector_store_stats,
            'top_k_retrieval': TOP_K_RETRIEVAL,
            'ollama_server': OLLAMA_BASE_URL
        }