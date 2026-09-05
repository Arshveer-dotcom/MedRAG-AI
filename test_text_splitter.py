#!/usr/bin/env python3
import sys
from pathlib import Path
from src.pdf_processor import PDFProcessor
from src.text_splitter import MedicalTextSplitter

def test_chunking():
    print("Testing Text Splitter...")
    
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
    
    print(f"\nChunking Results:")
    print(f"  Input pages: {len(pages)}")
    print(f"  Output chunks: {len(chunks)}")
    print(f"  Chunk size: 500 characters")
    print(f"  Chunk overlap: 100 characters")
    
    print(f"\nFirst 3 chunks:")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n  Chunk {i+1}:")
        print(f"    ID: {chunk['chunk_id']}")
        print(f"    Document: {chunk['document_name']}")
        print(f"    Page: {chunk['page_number']}")
        print(f"    Chunk #: {chunk['chunk_number']}")
        print(f"    Text length: {len(chunk['text'])} characters")
        print(f"    Text preview: {chunk['text'][:100]}...")
    
    if len(chunks) >= 2:
        print(f"\n  Chunk overlap test:")
        chunk1_text = chunks[0]['text']
        chunk2_text = chunks[1]['text']
        
        overlap_found = False
        for i in range(len(chunk1_text)):
            if chunk1_text[i:] in chunk2_text:
                overlap_found = True
                print(f"    Overlap found between chunks 1 and 2")
                break
        
        if not overlap_found:
            print(f"    No overlap detected (might be expected with small documents)")
    
    return True

if __name__ == "__main__":
    success = test_chunking()
    sys.exit(0 if success else 1)