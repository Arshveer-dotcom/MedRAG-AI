import fitz
import os
from pathlib import Path
from typing import List, Dict, Any

class PDFProcessor:
    
    @staticmethod
    def extract_text_from_pdf(pdf_path: Path) -> List[Dict[str, Any]]:
        try:
            doc = fitz.open(pdf_path)
            pages = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                cleaned_text = PDFProcessor._clean_text(text)
                
                pages.append({
                    'document_name': pdf_path.name,
                    'document_path': str(pdf_path),
                    'page_number': page_num + 1,
                    'text': cleaned_text,
                    'total_pages': len(doc)
                })
            
            doc.close()
            return pages
            
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {str(e)}")
            return []
    
    @staticmethod
    def _clean_text(text: str) -> str:
        import re
        text = re.sub(r'\n\s*\n', '\n', text)
        text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    @staticmethod
    def process_medical_documents(docs_dir: Path) -> List[Dict[str, Any]]:
        all_pages = []
        
        if not docs_dir.exists():
            print(f"Directory {docs_dir} does not exist.")
            return all_pages
        
        pdf_files = list(docs_dir.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {docs_dir}")
            return all_pages
        
        for pdf_file in pdf_files:
            print(f"Processing: {pdf_file.name}")
            pages = PDFProcessor.extract_text_from_pdf(pdf_file)
            all_pages.extend(pages)
            print(f"  Extracted {len(pages)} pages from {pdf_file.name}")
        
        print(f"\nTotal: Processed {len(pdf_files)} PDFs, extracted {len(all_pages)} pages")
        return all_pages