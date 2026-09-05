#!/usr/bin/env python3
import sys
from pathlib import Path
from src.pdf_processor import PDFProcessor

def create_dummy_pdf():
    try:
        import fitz
        
        docs_dir = Path("data/medical_documents")
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        dummy_pdf_path = docs_dir / "sample_medical.pdf"
        
        doc = fitz.open()
        
        page = doc.new_page()
        text = "This is a sample medical document for testing.\n\nSymptoms: fever, cough, fatigue.\nDiagnosis: Common cold.\nTreatment: Rest and hydration."
        page.insert_text((72, 72), text, fontsize=12)
        
        doc.save(dummy_pdf_path)
        doc.close()
        
        print(f"Created dummy PDF: {dummy_pdf_path}")
        return dummy_pdf_path
        
    except ImportError:
        print("PyMuPDF not installed. Please install with: pip install pymupdf")
        return None

def test_pdf_processing():
    print("Testing PDF Processor...")
    
    docs_dir = Path("data/medical_documents")
    pdf_files = list(docs_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found. Creating a dummy PDF...")
        dummy_path = create_dummy_pdf()
        if dummy_path:
            pdf_files = [dummy_path]
        else:
            print("Failed to create dummy PDF. Please provide a PDF in data/medical_documents/")
            return False
    
    test_pdf = pdf_files[0]
    print(f"\nProcessing test PDF: {test_pdf.name}")
    
    pages = PDFProcessor.extract_text_from_pdf(test_pdf)
    
    if not pages:
        print("Failed to extract text from PDF")
        return False
    
    print(f"\nExtraction Results:")
    print(f"  Document: {pages[0]['document_name']}")
    print(f"  Total pages: {pages[0]['total_pages']}")
    print(f"  Pages processed: {len(pages)}")
    
    for i, page in enumerate(pages):
        print(f"\n  Page {page['page_number']}:")
        print(f"    Text length: {len(page['text'])} characters")
        print(f"    First 100 chars: {page['text'][:100]}...")
        print(f"    Metadata: document_name={page['document_name']}, page_number={page['page_number']}")
    
    return True

if __name__ == "__main__":
    success = test_pdf_processing()
    sys.exit(0 if success else 1)