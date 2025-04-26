import tkinter as tk
from src.ui import PdfMarkdownApp

def main():
    """Main entry point for the PDF to Markdown converter application."""
    root = tk.Tk()
    app = PdfMarkdownApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 