# Contributing to MedRAG AI

Thank you for your interest in contributing to MedRAG AI! This document provides guidelines and information for contributors.

## How to Contribute

### 1. Fork the Repository
- Fork the repository on GitHub
- Clone your fork locally

### 2. Set Up Development Environment
```bash
# Clone your fork
git clone https://github.com/yourusername/MedRAG-AI.git
cd MedRAG-AI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
# pip install pytest black flake8
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes
- Follow the existing code style
- Add comments for complex logic
- Update documentation if needed
- Add tests for new functionality

### 5. Test Your Changes
```bash
# Run existing tests
python3 test_pdf_processor.py
python3 test_text_splitter.py
python3 test_vector_store.py
python3 test_complete_application.py

# Run the application
./run.sh
```

### 6. Commit Changes
```bash
git add .
git commit -m "Add your descriptive commit message"
```

### 7. Push to GitHub
```bash
git push origin feature/your-feature-name
```

### 8. Create Pull Request
- Go to the original repository on GitHub
- Click "New Pull Request"
- Describe your changes and their purpose

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Keep functions focused and concise
- Add docstrings to public functions and classes

### Testing
- Add tests for new functionality
- Ensure all existing tests pass
- Test both success and error scenarios

### Documentation
- Update README.md if adding new features
- Add inline comments for complex logic
- Update any relevant documentation files

### Medical Safety
- **Never** add functionality that provides medical diagnosis
- **Always** include appropriate disclaimers
- **Always** recommend consulting healthcare professionals
- **Never** hallucinate or generate medical information

## Reporting Issues

### Bug Reports
- Use the GitHub issue tracker
- Describe the bug clearly
- Include steps to reproduce
- Include expected vs actual behavior
- Include system information (OS, Python version, etc.)

### Feature Requests
- Use the GitHub issue tracker
- Clearly describe the feature
- Explain why it would be useful
- Consider medical safety implications

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive experience for everyone.

### Our Standards
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

### Medical Responsibility
- This project is for educational purposes only
- Never provide medical advice through code
- Always emphasize consulting healthcare professionals
- Maintain strict safety guidelines

## Questions?

If you have questions about contributing, please open an issue or reach out to the maintainers.

Thank you for contributing to MedRAG AI!