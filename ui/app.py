import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os

from core.llm import LLMClient
from core.search import DuckDuckGoSearch, OMDBSearch, YouTubeSearch
from core.conversation import ConversationManager
from ui.components import ConversationDisplay, QueryInput
from ui.styles import ThemeManager

class RAGApp:
    def __init__(self, root):
        self.root = root
        
        self.root.title("Movie Research Assistant")
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon.ico")
    
        if os.path.exists(icon_path):
            self.root.iconbitmap(default=icon_path)
        else:
            print(f"Warning: Icon file not found at {icon_path}")
        
        ThemeManager.configure_ttk_styles()
        
        self.root.configure(background=ThemeManager.COLORS["background"])
        
        self.setup_tools()
        self.setup_ui()
    
    def setup_tools(self):
        try:
            self.llm = LLMClient()
            
            # Initialize all search tools
            tools = [DuckDuckGoSearch()]
            
            # # Try to initialize OMDB API tool
            # try:
            #     tools.append(OMDBSearch())
            # except ValueError as e:
            #     self.show_warning(f"OMDB API: {str(e)}")
            
            # Try to initialize YouTube API tool
            try:
                tools.append(YouTubeSearch())
            except ValueError as e:
                self.show_warning(f"YouTube API: {str(e)}")
            
            self.conversation = ConversationManager(tools, self.llm)
            
            active_tools = ", ".join([tool.name for tool in tools])
            self.status_message = f"Ready to assist you | Active tools: {active_tools}"
        except ValueError as e:
            messagebox.showerror("API Key Error", str(e))
            self.status_message = "⚠️ Error: API key missing"
            self.conversation = None
    
    def show_warning(self, message):
        messagebox.showwarning("API Key Warning", 
                              f"{message}\nSome features will be disabled.")
    
    def setup_ui(self):
        # Create main container with padding
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add the conversation display with weight=5 (takes more space)
        self.conversation_display = ConversationDisplay(main_frame)
        self.conversation_display.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Add input area with weight=1 (takes less space)
        self.query_input = QueryInput(
            main_frame, 
            submit_callback=self.handle_query,
            model_change_callback=self.update_model
        )
        self.query_input.pack(fill=tk.X)
        
        # Status bar with custom styling
        self.status_var = tk.StringVar(value=self.status_message)
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            style="Status.TLabel",
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_model(self, model_name):
        if self.llm:
            self.llm.set_model(model_name)
            self.status_var.set(f"Model changed to: {model_name}")
    
    def handle_query(self, query):
        if not self.conversation:
            messagebox.showerror("Configuration Error", "Conversation manager not initialized. Please check your API keys.")
            return
        
        self.status_var.set("🔄 Processing your query...")
        self.query_input.set_state(tk.DISABLED)
        
        threading.Thread(target=self._process_query_thread, args=(query,), daemon=True).start()
    
    def _process_query_thread(self, query):
        try:
            response, _ = self.conversation.process_query(query)
            self.root.after(0, self._update_ui_after_query)
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Processing Error", error_msg))
            self.root.after(0, self._update_ui_after_query)
    
    def _update_ui_after_query(self):
        if self.conversation:
            self.conversation_display.update_history(self.conversation.history)
        
        self.query_input.set_state(tk.NORMAL)
        self.query_input.query_entry.focus_set()
        
        self.status_var.set("✓ Ready to assist you")