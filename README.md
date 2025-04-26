# PDF to Markdown Converter

A modern, user-friendly tool for converting PDF files to Markdown format. Built with Python and Tkinter.

![Screenshot of the application](docs/screenshot.png)

## Features

- Convert PDF files to clean, readable Markdown
- Modern GUI with progress indication
- Background processing to keep UI responsive
- Keyboard shortcuts for common actions
- Monospace font support for better code readability
- Error handling with user-friendly messages

## Installation

### From PyPI

```bash
pip install pdf2md
```

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pdf2md.git
   cd pdf2md
   ```

2. Install in development mode:
   ```bash
   pip install .
   ```

## Usage

### GUI Mode

After installation, run the application:
```bash
pdf2md
```

Keyboard shortcuts:
- `Ctrl+O`: Open PDF file
- `Ctrl+R`: Convert to Markdown
- `Ctrl+C`: Copy selected text
- `Ctrl+A`: Select all text

### Command-line Usage

Convert a PDF file directly from the command line:
```bash
pdf2md input.pdf --output output.md
```

## Example

### Before (PDF)
![Sample PDF](docs/sample_pdf.png)

### After (Markdown)
```markdown
# Sample PDF

This is a sample PDF file with some text.

## Section 1

- Bullet point 1
- Bullet point 2

## Section 2

Some code:

```python
def hello():
    print("Hello, World!")
```
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