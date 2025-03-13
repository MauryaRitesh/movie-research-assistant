import tkinter as tk
from tkinter import scrolledtext, ttk
import webbrowser
import re
from ui.styles import apply_text_styles, ThemeManager

class ConversationDisplay(ttk.LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="Conversation History", padding=10, **kwargs)
        
        container = ttk.Frame(self, padding=5)
        container.pack(fill=tk.BOTH, expand=True)
        
        header_frame = ttk.Frame(container)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(
            header_frame, 
            text="🔍 Movie Assistant Chat",
            font=("Segoe UI", 12, "bold"),
            foreground=ThemeManager.COLORS["primary"]
        ).pack(side=tk.LEFT)
        
        self.history_text = scrolledtext.ScrolledText(
            container, 
            wrap=tk.WORD, 
            width=80, 
            height=20
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        apply_text_styles(self.history_text)
        
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
                self.history_text.insert(tk.END, "─" * 80 + "\n", "tool_header")
                
                tool_name = entry['tool']
                
                if tool_name == "YouTube Search":
                    self.history_text.insert(tk.END, f"🎬 Trailer Search: '{entry['query']}'\n", "tool_header")
                else:
                    self.history_text.insert(tk.END, f"{tool_name}: '{entry['query']}'\n", "tool_header")
                
                results = entry["results"].get("results", [])
                if results:
                    if tool_name == "DuckDuckGo Search":
                        self._insert_duckduckgo_results(results)
                    elif tool_name == "OMDB Search":
                        self._insert_omdb_results(results)
                    elif tool_name == "YouTube Search":
                        self._insert_youtube_results(results)
                else:
                    error = entry["results"].get("error", "No results found")
                    self.history_text.insert(tk.END, f"No results: {error}\n", "tool_error")
                
                self.history_text.insert(tk.END, "─" * 80 + "\n\n", "tool_header")
        
        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)
    
    def _insert_duckduckgo_results(self, results):
        self.history_text.insert(tk.END, "📊 IMDB Information:\n", "tool_section")
        
        movie_info = {}
        for result in results:
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            
            if "rating" in snippet.lower() and "rating" not in movie_info:
                rating_match = re.search(r'(\d+(\.\d+)?)/10', snippet)
                if rating_match:
                    movie_info["rating"] = rating_match.group(0)
                    
            if "release" in snippet.lower() and "release_date" not in movie_info:
                date_match = re.search(r'released on ([A-Za-z]+ \d+, \d{4})|(\d{1,2} [A-Za-z]+ \d{4})', snippet)
                if date_match:
                    movie_info["release_date"] = date_match.group(0)
                    
            if "direct" in snippet.lower() and "director" not in movie_info:
                dir_match = re.search(r'directed by ([A-Za-z ]+)', snippet)
                if dir_match:
                    movie_info["director"] = dir_match.group(1)
                    
            if "star" in snippet.lower() and "cast" not in movie_info:
                cast_match = re.search(r'starring ([A-Za-z ,]+)', snippet)
                if cast_match:
                    movie_info["cast"] = cast_match.group(1)
        
        if movie_info:
            main_title = results[0].get("title", "").split(" - ")[0] if results else "Movie/Show"
            self.history_text.insert(tk.END, f"📽️ {main_title}\n", "movie_title")
            
            if "rating" in movie_info:
                self.history_text.insert(tk.END, "Rating: ", "info_label")
                self.history_text.insert(tk.END, f"⭐ {movie_info['rating']}\n", "info_value_bold")
                
            if "release_date" in movie_info:
                self.history_text.insert(tk.END, "Released: ", "info_label")
                self.history_text.insert(tk.END, f"{movie_info['release_date']}\n", "info_value")
                
            if "director" in movie_info:
                self.history_text.insert(tk.END, "Director: ", "info_label")
                self.history_text.insert(tk.END, f"{movie_info['director']}\n", "info_value")
                
            if "cast" in movie_info:
                self.history_text.insert(tk.END, "Cast: ", "info_label")
                self.history_text.insert(tk.END, f"{movie_info['cast']}\n", "info_value")
            
            self.history_text.insert(tk.END, "\n", "tool_detail")
        
        self.history_text.insert(tk.END, "🔍 Search Results:\n", "results_header")
        
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
            
            link_tag = f"link_{i}_{hash(link)}"
            self.history_text.tag_add(link_tag, link_start, link_end)
            self.history_text.tag_config(link_tag, foreground=ThemeManager.COLORS["link"], underline=1)
            self.history_text.tag_bind(link_tag, "<Button-1>", lambda e, url=link: webbrowser.open(url))    

    def _insert_omdb_results(self, results):
        self.history_text.insert(tk.END, "🎬 Movie Details:\n", "tool_section")
        
        for i, result in enumerate(results, 1):
            title = result.get("title", "")
            year = result.get("year", "")
            rating = result.get("rating", "N/A")
            genre = result.get("genre", "")
            director = result.get("director", "")
            actors = result.get("actors", "")
            plot = result.get("plot", "")
            imdb_link = result.get("imdbLink", "")
            
            self.history_text.insert(tk.END, f"{i}. {title} ({year})\n", "tool_item")
            self.history_text.insert(tk.END, f"Rating: ⭐ {rating}/10 | Genre: {genre}\n", "tool_detail")
            self.history_text.insert(tk.END, f"Director: {director}\n", "tool_detail")
            self.history_text.insert(tk.END, f"Cast: {actors}\n", "tool_detail")
            self.history_text.insert(tk.END, f"Plot: {plot}\n", "tool_detail")
            self.history_text.insert(tk.END, f"IMDB: ", "tool_link_label")
            
            link_start = self.history_text.index(tk.INSERT)
            self.history_text.insert(tk.END, f"{imdb_link}\n\n", "tool_link")
            link_end = self.history_text.index(tk.INSERT)
            
            link_tag = f"imdb_link_{i}_{hash(imdb_link)}"
            self.history_text.tag_add(link_tag, link_start, link_end)
            self.history_text.tag_config(link_tag, foreground=ThemeManager.COLORS["link"], underline=1)
            self.history_text.tag_bind(link_tag, "<Button-1>", lambda e, url=imdb_link: webbrowser.open(url))
    
    def _insert_youtube_results(self, results):
        self.history_text.insert(tk.END, "🎥 Trailer:\n", "tool_section")
        
        for i, result in enumerate(results, 1):
            title = result.get("title", "")
            link = result.get("link", "")
            
            self.history_text.insert(tk.END, f"🎬 {title}\n", "tool_item")
            self.history_text.insert(tk.END, f"Watch Trailer: ", "tool_link_label")
            
            link_start = self.history_text.index(tk.INSERT)
            self.history_text.insert(tk.END, f"{link}\n\n", "tool_link")
            link_end = self.history_text.index(tk.INSERT)
            
            link_tag = f"youtube_link_{i}_{hash(link)}"
            self.history_text.tag_add(link_tag, link_start, link_end)
            self.history_text.tag_config(link_tag, foreground=ThemeManager.COLORS["link"], underline=1)
            self.history_text.tag_bind(link_tag, "<Button-1>", lambda e, url=link: webbrowser.open(url))

class QueryInput(ttk.Frame):
    def __init__(self, parent, submit_callback, model_change_callback, **kwargs):
        super().__init__(parent, padding=10, **kwargs)
        
        self.submit_callback = submit_callback
        
        ttk.Label(
            self, 
            text="💬 Ask about a movie or show:",
            font=("Segoe UI", 11, "bold"),
            foreground=ThemeManager.COLORS["primary"]
        ).pack(anchor=tk.W, pady=(0, 5))
        
        input_row = ttk.Frame(self)
        input_row.pack(fill=tk.X, expand=True, pady=(0, 10))
        
        self.query_entry = ttk.Entry(input_row, width=70)
        self.query_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.query_entry.bind("<Return>", self.on_submit)
        
        search_button = ttk.Button(
            input_row, 
            text="Search",
            style="Main.TButton",
            command=self.on_submit
        )
        search_button.pack(side=tk.RIGHT)
        
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
            state="readonly"
        )
        model_options['values'] = (
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        )
        model_options.pack(side=tk.LEFT, padx=(0, 5))
        model_options.bind("<<ComboboxSelected>>", lambda e: model_change_callback(self.model_var.get()))
        
        ttk.Label(
            self, 
            text="Try: 'Tell me about The Batman' or 'Show me information about Oppenheimer'",
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