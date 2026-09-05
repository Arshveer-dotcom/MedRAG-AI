#!/usr/bin/env python3
import sys
from pathlib import Path
from src.pdf_processor import PDFProcessor
from src.text_splitter import MedicalTextSplitter
from src.embeddings import MedicalEmbeddings
from src.vector_store import MedicalVectorStore
from src.retriever import MedicalRetriever
from src.config import CHROMA_PERSIST_DIRECTORY, CHROMA_COLLECTION_NAME, EMBEDDING_MODEL_NAME
import shutil

def test_complete_flow():
    print("Testing Complete Application Flow...")
    
    test_db_dir = Path("chroma_db_test_complete")
    if test_db_dir.exists():
        shutil.rmtree(test_db_dir)
        print("Cleaned up previous test database")
    
    import src.config as config
    original_persist_dir = config.CHROMA_PERSIST_DIRECTORY
    config.CHROMA_PERSIST_DIRECTORY = test_db_dir
    
    try:
        print("\n1. Testing PDF processing...")
        docs_dir = Path("data/medical_documents")
        pdf_files = list(docs_dir.glob("*.pdf"))
        
        if not pdf_files:
            print("No PDF files found. Run test_pdf_processor.py first to create dummy PDF.")
            return False
        
        test_pdf = pdf_files[0]
        pages = PDFProcessor.extract_text_from_pdf(test_pdf)
        print(f"   Extracted {len(pages)} pages from {test_pdf.name}")
        
        print("\n2. Testing text splitting...")
        splitter = MedicalTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_pages_into_chunks(pages)
        print(f"   Created {len(chunks)} chunks")
        
        print("\n3. Testing embeddings...")
        embeddings_model = MedicalEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        texts = [chunk['text'] for chunk in chunks]
        embeddings = embeddings_model.generate_embeddings(texts)
        print(f"   Generated {len(embeddings)} embeddings")
        
        print("\n4. Testing vector store...")
        vector_store = MedicalVectorStore(
            persist_directory=test_db_dir,
            collection_name=CHROMA_COLLECTION_NAME
        )
        num_added = vector_store.add_chunks(chunks, embeddings)
        print(f"   Added {num_added} documents to vector store")
        
        print("\n5. Testing retrieval...")
        retriever = MedicalRetriever(
            vector_store=vector_store,
            embeddings=embeddings_model
        )
        
        test_queries = [
            "What are the symptoms?",
            "How is it treated?",
            "What causes this condition?"
        ]
        
        for query in test_queries:
            relevant_chunks = retriever.retrieve_relevant_chunks(query, top_k=2)
            print(f"   Query: '{query}'")
            print(f"   Retrieved {len(relevant_chunks)} chunks")
            
            if relevant_chunks:
                context = retriever.format_context_for_llm(relevant_chunks)
                print(f"   Context length: {len(context)} characters")
        
        print("\n6. Testing context formatting...")
        if relevant_chunks:
            context = retriever.format_context_for_llm(relevant_chunks)
            print(f"   Formatted context preview:")
            print(f"   {context[:200]}..." if len(context) > 200 else f"   {context}")
        
        print("\n✓ Complete application flow test successful!")
        print("Note: LLM integration requires Ollama server running")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        config.CHROMA_PERSIST_DIRECTORY = original_persist_dir
        
        if test_db_dir.exists():
            shutil.rmtree(test_db_dir)
            print(f"\nCleaned up test database at {test_db_dir}")

if __name__ == "__main__":
    success = test_complete_flow()
    sys.exit(0 if success else 1)