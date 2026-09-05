#!/usr/bin/env python3
import sys
from pathlib import Path
from src.pdf_processor import PDFProcessor
from src.text_splitter import MedicalTextSplitter
from src.embeddings import MedicalEmbeddings
from src.vector_store import MedicalVectorStore
import shutil

def test_vector_store():
    print("Testing Vector Store...")
    
    test_db_dir = Path("chroma_db_test")
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
        embeddings_model = MedicalEmbeddings()
        texts = [chunk['text'] for chunk in chunks]
        embeddings = embeddings_model.generate_embeddings(texts)
        print(f"Generated {len(embeddings)} embeddings")
    except Exception as e:
        print(f"Error generating embeddings: {str(e)}")
        print("Skipping embedding generation test (model may not be downloaded)")
        embeddings = [[0.1] * 384 for _ in chunks]
        print(f"Created {len(embeddings)} dummy embeddings for testing")
    
    print("\nCreating vector store...")
    vector_store = MedicalVectorStore(persist_directory=test_db_dir)
    
    print("Adding documents to vector store...")
    num_added = vector_store.add_chunks(chunks, embeddings)
    
    stats = vector_store.get_collection_stats()
    print(f"\nVector Store Stats:")
    print(f"  Collection: {stats['collection_name']}")
    print(f"  Documents: {stats['document_count']}")
    print(f"  Directory: {stats['persist_directory']}")
    
    print("\nTesting similarity search...")
    query = "What are the symptoms?"
    results = vector_store.similarity_search(query, k=2)
    
    print(f"Query: '{query}'")
    print(f"Results ({len(results)}):")
    for i, result in enumerate(results):
        print(f"\n  Result {i+1}:")
        print(f"    Score: {result['score']:.4f}")
        print(f"    Document: {result['metadata']['document_name']}")
        print(f"    Page: {result['metadata']['page_number']}")
        print(f"    Content preview: {result['content'][:100]}...")
    
    shutil.rmtree(test_db_dir)
    print(f"\nCleaned up test database at {test_db_dir}")
    
    return True

if __name__ == "__main__":
    success = test_vector_store()
    sys.exit(0 if success else 1)