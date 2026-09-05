# MedRAG AI - Technical Architecture

## Overview

MedRAG AI implements a Retrieval-Augmented Generation (RAG) system specifically designed for medical information retrieval. The architecture ensures safe, accurate, and source-attributed responses by combining semantic search with local LLM inference.

## Core Components

### 1. Document Processing Layer

#### PDF Processor (`src/pdf_processor.py`)
- **Technology**: PyMuPDF (fitz)
- **Purpose**: Extract text from PDF documents
- **Features**:
  - Preserves page metadata (document name, page number)
  - Text cleaning and preprocessing
  - Handles multiple PDF files
  - Error handling for corrupted files

#### Text Splitter (`src/text_splitter.py`)
- **Technology**: LangChain RecursiveCharacterTextSplitter
- **Purpose**: Split documents into meaningful chunks
- **Configuration**:
  - Chunk size: 1000 characters (configurable)
  - Overlap: 200 characters (configurable)
  - Separators: paragraphs, sentences, words
- **Metadata**: Preserves document and page information for each chunk

### 2. Embedding Layer

#### Embeddings Generator (`src/embeddings.py`)
- **Technology**: Sentence Transformers (all-MiniLM-L6-v2)
- **Purpose**: Convert text to semantic vectors
- **Output**: 384-dimensional vectors
- **Features**:
  - Batch processing for efficiency
  - Handles single and multiple texts
  - Consistent vector dimensions

### 3. Vector Storage Layer

#### Vector Store (`src/vector_store.py`)
- **Technology**: ChromaDB
- **Purpose**: Store and retrieve embeddings
- **Features**:
  - Persistent storage (survives restarts)
  - Metadata filtering
  - Similarity search with scores
  - Collection management

### 4. Retrieval Layer

#### Retriever (`src/retriever.py`)
- **Technology**: Custom implementation with ChromaDB
- **Purpose**: Find relevant chunks for queries
- **Process**:
  1. Convert query to embedding
  2. Perform similarity search
  3. Retrieve top-k relevant chunks
  4. Format context with source information

### 5. Generation Layer

#### LLM Interface (`src/llm.py`)
- **Technology**: Ollama (llama3.2:3b)
- **Purpose**: Generate medical answers
- **Configuration**:
  - Temperature: 0.3 (deterministic)
  - Context window: 4096 tokens
  - Timeout: 120 seconds
- **Safety**: Strict prompt engineering to prevent hallucination

### 6. Orchestration Layer

#### RAG Pipeline (`src/rag_pipeline.py`)
- **Purpose**: Coordinate all components
- **Process**:
  1. Document ingestion
  2. Question processing
  3. Retrieval
  4. Context formatting
  5. Answer generation
  6. Source attribution

### 7. Interface Layer

#### Streamlit App (`app.py`)
- **Technology**: Streamlit
- **Purpose**: User interface
- **Features**:
  - Chat interface
  - File upload
  - Session history
  - Source display
  - Medical disclaimer

## Data Flow

```
User Query
    ↓
Embedding Generation (Sentence Transformers)
    ↓
Semantic Search (ChromaDB)
    ↓
Relevant Chunks Retrieval
    ↓
Context Formatting
    ↓
Prompt Construction
    ↓
LLM Generation (Ollama)
    ↓
Answer + Sources
    ↓
User Interface Display
```

## Configuration Management

### Environment Variables (`.env`)
- `OLLAMA_BASE_URL`: Ollama server endpoint
- `OLLAMA_MODEL`: LLM model name
- `EMBEDDING_MODEL_NAME`: Embedding model
- `CHROMA_PERSIST_DIRECTORY`: Vector DB storage
- `MAX_CHUNK_SIZE`: Text chunking size
- `CHUNK_OVERLAP`: Chunk overlap size
- `TOP_K_RETRIEVAL`: Number of chunks to retrieve

### Configuration Module (`src/config.py`)
- Loads environment variables
- Provides default values
- Centralizes configuration

## Medical Safety Architecture

### 1. Context-Only Generation
- LLM receives only retrieved context
- No access to external knowledge
- Prevents hallucination of medical information

### 2. Source Attribution
- Every answer includes document references
- Page numbers for verification
- Relevance scores for transparency

### 3. Built-in Disclaimers
- Prominent medical disclaimer
- Educational purpose emphasis
- Healthcare professional consultation recommendation

### 4. No Diagnosis Capability
- System explicitly cannot diagnose
- No treatment recommendations
- Information retrieval only

## Performance Considerations

### Embedding Generation
- Model: all-MiniLM-L6-v2 (80MB)
- Dimensions: 384
- Speed: ~1000 chunks/minute

### Vector Search
- ChromaDB with HNSW index
- Sub-linear search time
- Configurable accuracy/speed tradeoff

### LLM Inference
- Local processing (no API calls)
- Dependent on hardware
- Typical response time: 2-10 seconds

## Scalability

### Current Limitations
- Single-user sessions
- Local processing only
- Memory-dependent on host machine

### Potential Improvements
- Multi-user support
- Cloud deployment
- GPU acceleration
- Multiple LLM support
- Advanced caching

## Security Considerations

### Data Privacy
- All processing local
- No external API calls
- No data transmission
- User-controlled documents

### Medical Data Handling
- No patient data storage
- Educational content only
- No PHI (Protected Health Information)
- User responsibility emphasized

## Testing Strategy

### Unit Tests
- Individual component testing
- Mock external dependencies
- Edge case coverage

### Integration Tests
- Component interaction testing
- End-to-end pipeline testing
- Error scenario testing

### Manual Testing
- User interface testing
- Medical question validation
- Source attribution verification

## Deployment

### Local Development
```bash
# Start Ollama
ollama serve

# Start Streamlit
streamlit run app.py
```

### Production Considerations
- Reverse proxy (nginx)
- Process management (systemd)
- Monitoring and logging
- Backup strategies

## Future Enhancements

### Short-term
- Support for more document formats
- Advanced chunking strategies
- Caching for frequently asked questions
- Export conversation history

### Long-term
- Multi-modal support (images, tables)
- Integration with medical ontologies
- Federated learning capabilities
- Real-time medical literature updates

---

This architecture document is intended for technical interviews and portfolio demonstration. It shows understanding of RAG systems, medical AI safety, and software architecture principles.