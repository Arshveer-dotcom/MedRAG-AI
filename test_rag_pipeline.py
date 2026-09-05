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

def test_rag_pipeline():
    print("Testing RAG Pipeline...")
    
    test_db_dir = Path("chroma_db_test_pipeline")
    if test_db_dir.exists():
        shutil.rmtree(test_db_dir)
        print("Cleaned up previous test database")
    
    docs_dir = Path("data/medical_documents")
    pdf_files = list(docs_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found. Run test_pdf_processor.py first.")
        return False
    
    test_pdf = pdf_files[0]
    print(f"Processing PDF: {test_pdf.name}")
    
    pages = PDFProcessor.extract_text_from_pdf(test_pdf)
    if not pages:
        print("Failed to extract text from PDF")
        return False
    
    splitter = MedicalTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_pages_into_chunks(pages)
    
    if not chunks:
        print("No chunks created")
        return False
    
    print(f"Created {len(chunks)} chunks")
    
    print("\nGenerating embeddings...")
    try:
        embeddings_model = MedicalEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        texts = [chunk['text'] for chunk in chunks]
        embeddings = embeddings_model.generate_embeddings(texts)
        print(f"Generated {len(embeddings)} embeddings")
    except Exception as e:
        print(f"Error generating embeddings: {str(e)}")
        return False
    
    print("\nCreating vector store...")
    vector_store = MedicalVectorStore(
        persist_directory=test_db_dir,
        collection_name=CHROMA_COLLECTION_NAME
    )
    
    print("Adding documents to vector store...")
    num_added = vector_store.add_chunks(chunks, embeddings)
    
    print("\nCreating retriever...")
    retriever = MedicalRetriever(
        vector_store=vector_store,
        embeddings=embeddings_model
    )
    
    print("\nTesting retrieval...")
    query = "What are the symptoms of common cold?"
    relevant_chunks = retriever.retrieve_relevant_chunks(query, top_k=3)
    
    print(f"Query: '{query}'")
    print(f"Retrieved {len(relevant_chunks)} chunks")
    
    for i, chunk in enumerate(relevant_chunks):
        print(f"\n  Chunk {i+1}:")
        print(f"    Score: {chunk['score']:.4f}")
        print(f"    Document: {chunk['metadata']['document_name']}")
        print(f"    Page: {chunk['metadata']['page_number']}")
        print(f"    Content: {chunk['content'][:100]}...")
    
    context = retriever.format_context_for_llm(relevant_chunks)
    print(f"\nFormatted Context:")
    print(context[:200] + "..." if len(context) > 200 else context)
    
    shutil.rmtree(test_db_dir)
    print(f"\nCleaned up test database at {test_db_dir}")
    
    print("\n✓ RAG pipeline components tested successfully")
    print("Note: LLM test requires Ollama server running (Stage 7)")
    
    return True

if __name__ == "__main__":
    success = test_rag_pipeline()
    sys.exit(0 if success else 1)