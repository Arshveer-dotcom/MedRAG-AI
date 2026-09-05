from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict, Any

class MedicalTextSplitter:
    """Splits medical documents into meaningful overlapping chunks."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def split_pages_into_chunks(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunks = []
        
        for page in pages:
            page_chunks = self._split_single_page(page)
            chunks.extend(page_chunks)
        
        print(f"Split {len(pages)} pages into {len(chunks)} chunks")
        return chunks
    
    def _split_single_page(self, page: Dict[str, Any]) -> List[Dict[str, Any]]:
        text = page['text']
        
        if not text.strip():
            return []
        
        text_chunks = self.text_splitter.split_text(text)
        
        chunks = []
        for i, chunk_text in enumerate(text_chunks):
            chunk = {
                'chunk_id': f"{page['document_name']}_page{page['page_number']}_chunk{i}",
                'document_name': page['document_name'],
                'document_path': page['document_path'],
                'page_number': page['page_number'],
                'chunk_number': i,
                'text': chunk_text,
                'total_chunks_on_page': len(text_chunks),
                'total_pages': page['total_pages']
            }
            chunks.append(chunk)
        
        return chunks