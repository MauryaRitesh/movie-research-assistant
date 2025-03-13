import tkinter as tk
from tkinter import scrolledtext, ttk
import webbrowser
from ui.styles import apply_text_styles, ThemeManager

class ConversationDisplay(ttk.LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Conversation History", padding=10, **kwargs)
        
        # Create a frame with padding for the text widget
        container = ttk.Frame(self, padding=5)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Add header frame with icon (can be expanded later)
        header_frame = ttk.Frame(container)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(
            header_frame, 
            text="🔍 RAG Assistant Chat",
            font=("Segoe UI", 12, "bold"),
            foreground=ThemeManager.COLORS["primary"]
        ).pack(side=tk.LEFT)
        
        # Create scrolled text with styling
        self.history_text = scrolledtext.ScrolledText(
            container, 
            wrap=tk.WORD, 
            width=80, 
            height=20
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Apply the text styling
        apply_text_styles(self.history_text)
        
        # Set initial state
        self.history_text.config(state=tk.DISABLED)
        
    def update_history(self, conversation_history):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        for entry in conversation_history:
            if entry["role"] == "user":
                self.history_text.insert(tk.END, "You: ", "user")
                self.history_text.insert(tk.END, f"{entry['content']}\n\n", "user")
            elif entry["role"] == "assistant":
                self.history_text.insert(tk.END, "Assistant: ", "assistant")
                self.history_text.insert(tk.END, f"{entry['content']}\n\n", "assistant")
            elif entry["role"] == "tool":
                # Add a separator line before tool results
                self.history_text.insert(tk.END, "─" * 80 + "\n", "tool_header")
                self.history_text.insert(tk.END, f"Search Results: '{entry['query']}' via {entry['tool']}\n", "tool_header")
                
                results = entry["results"].get("results", [])
                if results:
                    for i, result in enumerate(results, 1):
                        title = result.get("title", "")
                        snippet = result.get("snippet", "")
                        link = result.get("link", "")
                        
                        self.history_text.insert(tk.END, f"{i}. {title}\n", "tool_item")
                        self.history_text.insert(tk.END, f"{snippet}\n", "tool_detail")
                        self.history_text.insert(tk.END, f"Source: ", "tool_link_label")
                        
                        link_start = self.history_text.index(tk.INSERT)
                        self.history_text.insert(tk.END, f"{link}\n\n", "tool_link")
                        link_end = self.history_text.index(tk.INSERT)
                        
                        link_tag = f"link_{link}"
                        self.history_text.tag_add(link_tag, link_start, link_end)
                        self.history_text.tag_config(link_tag, foreground=ThemeManager.COLORS["link"], underline=1)
                        self.history_text.tag_bind(link_tag, "<Button-1>", lambda e, url=link: webbrowser.open(url))
                else:
                    error = entry["results"].get("error", "No results found")
                    self.history_text.insert(tk.END, f"No results: {error}\n", "tool_error")
                
                # Add a separator line after tool results
                self.history_text.insert(tk.END, "─" * 80 + "\n\n", "tool_header")
        
        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)

class QueryInput(ttk.Frame):
    def __init__(self, parent, submit_callback, model_change_callback, **kwargs):
        super().__init__(parent, padding=10, **kwargs)
        
        self.submit_callback = submit_callback
        
        # Main label with icon
        ttk.Label(
            self, 
            text="💬 Ask a question:",
            font=("Segoe UI", 11, "bold"),
            foreground=ThemeManager.COLORS["primary"]
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # Input row with text entry and button
        input_row = ttk.Frame(self)
        input_row.pack(fill=tk.X, expand=True, pady=(0, 10))
        
        self.query_entry = ttk.Entry(input_row, width=70)
        self.query_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.query_entry.bind("<Return>", self.on_submit)
        
        # Style the search button
        search_button = ttk.Button(
            input_row, 
            text="Search",
            style="Main.TButton",
            command=self.on_submit
        )
        search_button.pack(side=tk.RIGHT)
        
        # Model selection with background frame
        model_frame = ttk.Frame(self, padding=5)
        model_frame.pack(fill=tk.X, expand=True, pady=(0, 5))
        
        model_label = ttk.Label(
            model_frame, 
            text="🤖 Model:",
            font=("Segoe UI", 10),
            foreground=ThemeManager.COLORS["secondary"]
        )
        model_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.model_var = tk.StringVar(value="llama3-70b-8192")
        model_options = ttk.Combobox(
            model_frame, 
            textvariable=self.model_var, 
            width=30,
            state="readonly"  # Make it readonly for better UI
        )
        model_options['values'] = (
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        )
        model_options.pack(side=tk.LEFT, padx=(0, 5))
        model_options.bind("<<ComboboxSelected>>", lambda e: model_change_callback(self.model_var.get()))
        
        # Hint text under input
        ttk.Label(
            self, 
            text="Tip: Ask specific questions for better results",
            font=("Segoe UI", 9, "italic"),
            foreground=ThemeManager.COLORS["text_light"]
        ).pack(anchor=tk.W)
        
        self.query_entry.focus_set()
    
    def on_submit(self, event=None):
        query = self.query_entry.get().strip()
        if query:
            self.submit_callback(query)
            self.query_entry.delete(0, tk.END)
    
    def set_state(self, state):
        self.query_entry.config(state=state)