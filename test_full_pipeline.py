#!/usr/bin/env python3
import sys
from pathlib import Path
from src.rag_pipeline import MedicalRAGPipeline
import shutil

def test_full_pipeline():
    print("Testing Complete RAG Pipeline...")
    
    test_db_dir = Path("chroma_db_test_full")
    if test_db_dir.exists():
        shutil.rmtree(test_db_dir)
        print("Cleaned up previous test database")
    
    import src.config as config
    config.CHROMA_PERSIST_DIRECTORY = test_db_dir
    
    print("\n1. Initializing RAG pipeline...")
    try:
        pipeline = MedicalRAGPipeline()
    except Exception as e:
        print(f"Failed to initialize pipeline: {str(e)}")
        print("Make sure Ollama server is running and model is pulled")
        return False
    
    print("\n2. Ingesting documents...")
    docs_dir = Path("data/medical_documents")
    
    if not docs_dir.exists():
        print(f"Documents directory does not exist: {docs_dir}")
        return False
    
    num_chunks = pipeline.ingest_documents(docs_dir)
    
    if num_chunks == 0:
        print("No chunks were added to vector store")
        return False
    
    print("\n3. Testing question answering...")
    test_questions = [
        "What are the symptoms of common cold?",
        "How is common cold treated?",
        "What is the diagnosis for fever and cough?"
    ]
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        result = pipeline.answer_question(question)
        
        print(f"Answer: {result['answer'][:200]}...")
        print(f"Sources: {len(result['sources'])} source(s)")
        
        for source in result['sources']:
            print(f"  - {source['document_name']}, Page {source['page_number']}")
    
    print("\n4. Pipeline Information:")
    info = pipeline.get_pipeline_info()
    print(f"  Embedding model: {info['embedding_model']}")
    print(f"  LLM model: {info['llm_model']}")
    print(f"  Vector store documents: {info['vector_store']['document_count']}")
    
    shutil.rmtree(test_db_dir)
    print(f"\nCleaned up test database at {test_db_dir}")
    
    print("\n✓ Complete RAG pipeline test successful!")
    return True

if __name__ == "__main__":
    success = test_full_pipeline()
    sys.exit(0 if success else 1)