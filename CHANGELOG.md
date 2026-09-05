# Changelog

All notable changes to MedRAG AI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- PDF text extraction with PyMuPDF
- Document chunking with LangChain
- Embedding generation with Sentence Transformers
- Vector storage with ChromaDB
- Semantic retrieval system
- Ollama LLM integration
- Complete RAG pipeline
- Streamlit chat interface
- Medical-themed UI design
- Source attribution system
- Session chat history
- Medical disclaimer
- Configuration management with .env
- Test suite for all components
- Startup script for easy launching
- Comprehensive documentation

### Changed
- Updated README with complete documentation
- Enhanced .gitignore for Python projects
- Improved error handling throughout

### Fixed
- Initial bug fixes and stability improvements

## [0.1.0] - 2026-09-04

### Added
- Core RAG pipeline implementation
- PDF processing and text extraction
- ChromaDB vector storage integration
- Sentence Transformers embeddings
- Ollama LLM integration
- Streamlit chat interface
- Medical-themed user interface
- Source citation system
- Session management
- Configuration system
- Test suite
- Documentation

### Technical Details
- Uses all-MiniLM-L6-v2 for embeddings (384 dimensions)
- Default chunk size: 1000 characters with 200 overlap
- ChromaDB for persistent vector storage
- Ollama with llama3.2:3b for local LLM inference
- Streamlit for web-based chat interface

### Medical Safety
- Built-in medical disclaimer
- Source attribution for all answers
- Context-only generation to reduce hallucination
- Educational purpose emphasis

---

## How to Update This File

When adding new features or making changes:

1. Add a new entry under `[Unreleased]`
2. Categorize changes as Added, Changed, Deprecated, Removed, Fixed, or Security
3. Include relevant details and issue numbers
4. When releasing a new version, move `[Unreleased]` content to a new version section

For more information on Keep a Changelog format, visit: https://keepachangelog.com/en/1.0.0/