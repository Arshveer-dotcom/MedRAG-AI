# MedRAG AI - Medical Information Assistant

An AI-powered medical information chatbot using Retrieval-Augmented Generation (RAG) that answers questions based on a curated medical knowledge base.

## ⚠️ Medical Disclaimer

**This chatbot provides general medical information for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. If you have a medical concern, consult a qualified healthcare professional.**

## 🎯 Project Overview

MedRAG AI is a portfolio-ready demonstration of how RAG technology can be applied to medical information retrieval. The system allows users to upload medical PDF documents, processes them into a searchable knowledge base, and answers questions using only the provided context - reducing hallucination and ensuring source attribution.

### Key Highlights
- **No API keys required** - Runs entirely locally using Ollama
- **Source attribution** - Every answer includes document and page references
- **Hallucination reduction** - Answers strictly from provided context
- **Medical safety** - Built-in disclaimers and limitations

## ✨ Features

- 📄 **PDF Upload & Processing** - Extract text from medical PDFs with metadata preservation
- 🔍 **Semantic Search** - Find relevant information using vector embeddings
- 🤖 **Local LLM Integration** - Uses Ollama for private, offline AI responses
- 📚 **Source Citations** - Every answer includes document name and page number
- 💬 **Chat Interface** - Modern Streamlit-based conversational UI
- 📜 **Session History** - Maintains conversation context within sessions
- 🏥 **Medical Theme** - Clean, professional medical-themed interface
- ⚠️ **Safety First** - Built-in disclaimers and responsible AI practices

## 🏗️ Architecture

```
Medical PDFs
    ↓
PDF Text Extraction (PyMuPDF)
    ↓
Text Cleaning & Preprocessing
    ↓
Document Chunking (LangChain)
    ↓
Embedding Generation (Sentence Transformers)
    ↓
Vector Storage (ChromaDB)
    ↓
Semantic Retrieval
    ↓
Context Formatting
    ↓
LLM Response Generation (Ollama)
    ↓
Answer + Source Citations
```

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Web-based chat interface |
| **PDF Processing** | PyMuPDF (fitz) | Text extraction from PDFs |
| **Text Splitting** | LangChain | Document chunking with overlap |
| **Embeddings** | Sentence Transformers | Generate semantic vectors |
| **Vector Database** | ChromaDB | Store and retrieve embeddings |
| **LLM** | Ollama (llama3.2:3b) | Generate medical answers |
| **Orchestration** | LangChain | RAG pipeline management |
| **Configuration** | python-dotenv | Environment variable management |

## 📁 Project Structure

```
MedRAG-AI/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
├── run.sh                     # Startup script
│
├── data/
│   └── medical_documents/     # PDF storage directory
│
├── chroma_db/                 # Persistent vector database
│
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── pdf_processor.py       # PDF text extraction
│   ├── text_splitter.py       # Document chunking
│   ├── embeddings.py          # Embedding generation
│   ├── vector_store.py        # ChromaDB integration
│   ├── retriever.py           # Semantic retrieval
│   ├── llm.py                 # Ollama LLM integration
│   └── rag_pipeline.py        # Complete RAG pipeline
│
└── utils/
    └── helpers.py             # Utility functions
```

## 🚀 Installation

### Prerequisites
- Python 3.9+
- Ollama (for local LLM)
- 8GB+ RAM recommended

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/MedRAG-AI.git
cd MedRAG-AI
```

### Step 2: Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### Step 3: Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure environment
```bash
cp .env.example .env
# Edit .env if you want to change default settings
```

## 🦙 Ollama Setup

### Install Ollama
```bash
# macOS
brew install ollama

# Or visit https://ollama.ai for other platforms
```

### Start Ollama server
```bash
ollama serve
```

### Pull the required model
```bash
ollama pull llama3.2:3b
```

### Verify installation
```bash
python3 test_ollama.py
```

## 💻 How to Run

### Quick Start
```bash
# Make the startup script executable
chmod +x run.sh

# Run the application
./run.sh
```

### Manual Start
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Streamlit app
source venv/bin/activate
streamlit run app.py
```

### Access the application
Open your browser and navigate to: `http://localhost:8501`

## 📚 How RAG Works in This Project

### 1. Document Ingestion
- User uploads medical PDF documents
- PyMuPDF extracts text while preserving page metadata
- Text is cleaned and preprocessed

### 2. Chunking
- Documents are split into overlapping chunks (default: 1000 chars, 200 overlap)
- Preserves document and page information for each chunk
- Uses LangChain's RecursiveCharacterTextSplitter

### 3. Embedding Generation
- Each chunk is converted to a 384-dimensional vector using all-MiniLM-L6-v2
- Captures semantic meaning of medical text

### 4. Vector Storage
- Embeddings are stored in ChromaDB with persistent storage
- Maintains metadata for source attribution

### 5. Semantic Retrieval
- User question is converted to an embedding
- ChromaDB finds most similar chunks using cosine similarity
- Returns top-k relevant chunks (default: 5)

### 6. Context-Aware Generation
- Retrieved chunks are formatted as context
- LLM receives only the relevant context (not the entire knowledge base)
- Generates answer strictly based on provided context

### 7. Source Attribution
- Each answer includes document names and page numbers
- Users can verify information from original sources

## 💡 Example Questions

Once you've uploaded medical documents, try these questions:

**Symptoms:**
- "What are the symptoms of diabetes?"
- "How does hypertension present itself?"
- "What are the warning signs of a heart attack?"

**Treatments:**
- "How is type 2 diabetes treated?"
- "What are the treatment options for migraines?"
- "What medications are used for high blood pressure?"

**General Information:**
- "What causes asthma?"
- "How is cholesterol measured?"
- "What is the difference between type 1 and type 2 diabetes?"

**Note:** Answers depend on the content of your uploaded PDF documents.

## ⚠️ Limitations

1. **Knowledge Base Dependent** - Can only answer based on uploaded documents
2. **No Real-time Data** - Cannot access current medical research or news
3. **No Diagnosis** - Cannot diagnose conditions or recommend treatments
4. **No Patient Context** - Doesn't consider individual patient history
5. **PDF Only** - Currently supports PDF documents only
6. **Local Processing** - Requires sufficient RAM for LLM and embeddings
7. **Model Dependent** - Answer quality depends on the chosen LLM

## 🔒 Safety Considerations

- **No Medical Advice** - System explicitly states it's for educational purposes only
- **Source Attribution** - All answers include references for verification
- **Hallucination Reduction** - Strict context-only generation
- **Local Processing** - No data sent to external servers
- **User Responsibility** - Clear disclaimers about consulting healthcare professionals

## 🧪 Testing

Run the test suite to verify components:

```bash
# Test PDF processing
python3 test_pdf_processor.py

# Test text splitting
python3 test_text_splitter.py

# Test embeddings and vector store
python3 test_vector_store.py

# Test complete pipeline
python3 test_complete_application.py

# Test Ollama connection
python3 test_ollama.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for local LLM infrastructure
- [LangChain](https://langchain.com) for RAG framework
- [ChromaDB](https://www.trychroma.com) for vector storage
- [Sentence Transformers](https://www.sbert.net) for embeddings
- [Streamlit](https://streamlit.io) for the web interface
- [PyMuPDF](https://pymupdf.readthedocs.io) for PDF processing

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Remember: This is an educational project demonstrating RAG technology. Always consult qualified healthcare professionals for medical advice.**# MedRAG-AI
