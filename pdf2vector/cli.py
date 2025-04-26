"""
CLI module for pdf2vector.

This module provides a command-line interface for the application.
"""

import os
import logging
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn

from .core.app import PDF2Vector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("pdf2vector")
console = Console()

app = typer.Typer(
    name="pdf2vector",
    help="Convert PDFs to vector embeddings for semantic search and RAG applications",
    add_completion=False
)

@app.command()
def watch(
    input_dir: str = typer.Option(
        "input_pdfs",
        "--input-dir",
        "-i",
        help="Directory to watch for PDF files"
    ),
    persist_dir: str = typer.Option(
        ".chroma",
        "--persist-dir",
        "-p",
        help="Directory to persist the vector store"
    )
):
    """Watch a directory for PDF files and process them."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Starting PDF2Vector...", total=None)
            
            # Initialize application
            pdf2vector = PDF2Vector(
                input_dir=input_dir,
                persist_dir=persist_dir
            )
            
            progress.update(task, description="Watching for PDF files...")
            
            # Keep the application running
            try:
                while True:
                    console.print("\nEnter your question (or 'exit' to quit):")
                    question = input().strip()
                    
                    if question.lower() == "exit":
                        break
                        
                    if not question:
                        continue
                        
                    # Get answer
                    response = pdf2vector.ask_question(question)
                    
                    # Print answer
                    console.print("\n[bold green]Answer:[/bold green]")
                    console.print(response["answer"])
                    
                    # Print sources
                    console.print("\n[bold blue]Sources:[/bold blue]")
                    for source in response["sources"]:
                        console.print(
                            f"- {source['filename']} (Chunk {source['chunk_index']})"
                        )
                        console.print(f"  {source['text'][:200]}...")
                        
            except KeyboardInterrupt:
                console.print("\n[yellow]Stopping PDF2Vector...[/yellow]")
                
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise typer.Exit(1)

@app.command()
def process(
    pdf_path: str = typer.Argument(..., help="Path to the PDF file to process"),
    input_dir: str = typer.Option(
        "input_pdfs",
        "--input-dir",
        "-i",
        help="Directory to watch for PDF files"
    ),
    persist_dir: str = typer.Option(
        ".chroma",
        "--persist-dir",
        "-p",
        help="Directory to persist the vector store"
    )
):
    """Process a single PDF file."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Processing PDF...", total=None)
            
            # Initialize application
            pdf2vector = PDF2Vector(
                input_dir=input_dir,
                persist_dir=persist_dir
            )
            
            # Process PDF
            pdf_path = Path(pdf_path)
            pdf2vector.process_pdf(pdf_path)
            
            progress.update(task, description="Done!")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 