# PDF to Vector Converter

A modern tool for converting PDF files to vector embeddings for semantic search and RAG applications. Built with Python.

## Features

- Convert PDF files to vector embeddings
- Automatic PDF processing with folder watching
- Semantic search across processed documents
- Question answering using document context
- Persistent vector storage with ChromaDB
- Modern CLI interface with rich output

## Installation

### From PyPI

```bash
pip install pdf2vector
```

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pdf2vector.git
   cd pdf2vector
   ```

2. Install in development mode:
   ```bash
   pip install .
   ```

## Usage

### Watch Mode

Watch a directory for new PDF files and process them automatically:

```bash
pdf2vector watch --input-dir input_pdfs --persist-dir .chroma
```

This will:
1. Watch the `input_pdfs` directory for new PDF files
2. Process any new PDFs automatically
3. Store the vectors in the `.chroma` directory
4. Allow you to ask questions about the processed documents

### Process Single PDF

Process a single PDF file:

```bash
pdf2vector process input.pdf --input-dir input_pdfs --persist-dir .chroma
```

### Example Usage

1. Start watching for PDFs:
   ```bash
   pdf2vector watch
   ```

2. Drop a PDF file into the `input_pdfs` directory

3. Ask questions about the content:
   ```
   Enter your question: What are the main topics covered in the document?
   ```

4. Get answers with sources:
   ```
   Answer: Here are the relevant passages from the documents:
   
   Sources:
   - document.pdf (Chunk 1)
     The main topics covered in this document are...
   - document.pdf (Chunk 2)
     Additionally, the document discusses...
   ```

## Development

### Setup Development Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\activate  # Windows
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests

```bash
pytest tests/
```

### Code Quality

- Format code: `black .`
- Type checking: `mypy src tests`
- Linting: `flake8`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history. 