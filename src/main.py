"""Main entry point for the PDF to Markdown Converter."""
import sys
import tkinter as tk

from .ui import PdfMarkdownApp

def main():
    """Run the PDF to Markdown Converter application."""
    root = tk.Tk()
    app = PdfMarkdownApp(root)
    root.mainloop()

if __name__ == "__main__":
    sys.exit(main()) 