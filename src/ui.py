import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path
from typing import Optional

from .converter import convert_pdf_to_markdown, ConversionError

logger = logging.getLogger(__name__)

class PdfMarkdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Markdown Converter")
        self.root.geometry("800x600")
        
        # Variables
        self.selected_file_path: Optional[Path] = None
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.current_future = None
        
        # Create widgets
        self.create_widgets()
        self.setup_keyboard_shortcuts()
        
        # Configure grid weights
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_widgets(self):
        # Menu bar
        self.create_menu()
        
        # File selection frame
        file_frame = tk.Frame(self.root)
        file_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        self.select_button = tk.Button(
            file_frame,
            text="Select PDF (Ctrl+O)",
            command=self.select_file
        )
        self.select_button.pack(side=tk.LEFT, padx=5)
        
        self.file_label = tk.Label(
            file_frame,
            text="No file selected",
            wraplength=500
        )
        self.file_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Convert button
        self.convert_button = tk.Button(
            self.root,
            text="Convert to Markdown (Ctrl+R)",
            command=self.convert_file,
            state=tk.DISABLED
        )
        self.convert_button.grid(row=1, column=0, padx=10, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.root,
            variable=self.progress_var,
            mode='indeterminate'
        )
        self.progress_bar.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")
        self.progress_bar.grid_remove()  # Hidden by default
        
        # Text area with monospace font
        self.text_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=('Courier', 10)  # Monospace font
        )
        self.text_area.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open (Ctrl+O)", command=self.select_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Select All", command=lambda: self.text_area.tag_add(tk.SEL, "1.0", tk.END))
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Monospace Font", command=self.toggle_monospace_font)
        
    def setup_keyboard_shortcuts(self):
        self.root.bind('<Control-o>', lambda e: self.select_file())
        self.root.bind('<Control-r>', lambda e: self.convert_file())
        
    def toggle_monospace_font(self):
        current_font = self.text_area.cget("font")
        if "Courier" in str(current_font):
            self.text_area.configure(font=('TkDefaultFont', 10))
        else:
            self.text_area.configure(font=('Courier', 10))
            
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            self.selected_file_path = Path(file_path)
            self.file_label.config(text=str(self.selected_file_path))
            self.convert_button.config(state=tk.NORMAL)
            self.status_label.config(text="File selected. Ready to convert.")
            
    def convert_file(self):
        if not self.selected_file_path:
            messagebox.showerror(
                "Error",
                "Please select a PDF file first."
            )
            return
            
        self.convert_button.config(state=tk.DISABLED)
        self.status_label.config(text="Converting...")
        self.text_area.delete(1.0, tk.END)
        self.progress_bar.grid()
        self.progress_bar.start()
        
        def conversion_task():
            try:
                result = convert_pdf_to_markdown(str(self.selected_file_path))
                return result, None
            except Exception as e:
                return None, e
                
        def update_ui(future):
            self.progress_bar.stop()
            self.progress_bar.grid_remove()
            self.convert_button.config(state=tk.NORMAL)
            
            try:
                result, error = future.result()
                if error:
                    raise error
                    
                self.text_area.insert(tk.END, result)
                self.status_label.config(text="Conversion complete.")
                
            except ConversionError as e:
                error_msg = str(e)
                self.status_label.config(text="Error during conversion.")
                messagebox.showerror("Conversion Error", error_msg)
                self.text_area.insert(tk.END, f"# Error: {error_msg}")
                
            except Exception as e:
                error_msg = str(e)
                self.status_label.config(text="Error during conversion.")
                messagebox.showerror("Conversion Error", error_msg)
                self.text_area.insert(tk.END, f"# Error: {error_msg}")
                
            finally:
                self.current_future = None
                
        self.current_future = self.executor.submit(conversion_task)
        self.current_future.add_done_callback(update_ui)
        
    def __del__(self):
        self.executor.shutdown(wait=False) 