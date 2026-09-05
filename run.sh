#!/bin/bash

echo "Starting MedRAG AI..."

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Warning: Ollama server not detected."
    echo "Please start Ollama in another terminal:"
    echo "  ollama serve"
    echo ""
    echo "Then pull the required model:"
    echo "  ollama pull llama3.2:3b"
    echo ""
fi

echo "Starting Streamlit app..."
echo "Open http://localhost:8501 in your browser"
streamlit run app.py --server.port 8501 --server.address localhost
