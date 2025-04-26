# PDF to Markdown Converter

A Python application that converts PDF files to Markdown format using a graphical user interface. Built with Tkinter and the markitdown library, it provides a simple and intuitive way to convert PDF documents while maintaining text formatting and structure.

## Features

- User-friendly graphical interface
- Simple file selection through a file dialog
- One-click PDF to Markdown conversion
- Real-time display of converted Markdown text
- Status updates and error handling
- Copy converted text to clipboard functionality

## Requirements

- Python 3.x
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pdf-to-markdown-converter
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Activate the virtual environment if not already activated:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Run the application:
   ```bash
   python src/main.py
   ```

3. Use the GUI:
   - Click "Select PDF" to choose a PDF file
   - Click "Convert" to transform the PDF to Markdown
   - The converted text will appear in the text area
   - Use "Copy to Clipboard" to copy the converted text
   - Click "Clear" to reset the application

## Error Handling

The application provides clear error messages for common issues:
- File not found errors
- Conversion failures
- Invalid file formats
- Library dependency issues

All errors are displayed directly in the application interface.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 