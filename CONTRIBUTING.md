# Contributing to PDF to Markdown Converter

Thank you for your interest in contributing to PDF to Markdown Converter! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/pdf2md.git`
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\activate  # Windows
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests and checks:
   ```bash
   # Run tests
   pytest tests/
   
   # Format code
   black .
   
   # Type checking
   mypy src tests
   
   # Linting
   flake8
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

## Pull Request Guidelines

- Provide a clear description of the changes
- Include tests for new features
- Update documentation as needed
- Ensure all tests pass
- Follow the code style guidelines

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes
- Keep functions focused and small
- Use meaningful variable names

## Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for good test coverage
- Use pytest fixtures when appropriate

## Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Update CHANGELOG.md for significant changes
- Include examples for new features

## Questions?

Feel free to open an issue for any questions or discussions. 