import tkinter as tk
from tkinter import ttk

class ThemeManager:
    COLORS = {
        "primary": "#2c3e50",
        "secondary": "#34495e",
        "accent": "#3498db",
        "background": "#f5f5f5",
        "text": "#333333",
        "text_light": "#7f8c8d",
        "success": "#27ae60",
        "error": "#e74c3c",
        "warning": "#f39c12",
        "link": "#2980b9",
        "border": "#bdc3c7",
        "highlight": "#e6f3fc"
    }
    
    @staticmethod
    def configure_ttk_styles():
        style = ttk.Style()
        
        # General application style
        style.configure("TFrame", background=ThemeManager.COLORS["background"])
        style.configure("TLabel", background=ThemeManager.COLORS["background"], foreground=ThemeManager.COLORS["text"])
        style.configure("TButton", 
                        background=ThemeManager.COLORS["accent"], 
                        foreground="white", 
                        font=("Segoe UI", 10),
                        padding=6)
        style.map("TButton",
                 background=[("active", ThemeManager.COLORS["link"])],
                 relief=[("pressed", "sunken")])
        
        # LabelFrame
        style.configure("TLabelframe", 
                       background=ThemeManager.COLORS["background"],
                       foreground=ThemeManager.COLORS["primary"])
        style.configure("TLabelframe.Label", 
                       font=("Segoe UI", 11, "bold"),
                       background=ThemeManager.COLORS["background"],
                       foreground=ThemeManager.COLORS["primary"])
        
        # Entry widget
        style.configure("TEntry", 
                       foreground=ThemeManager.COLORS["text"],
                       fieldbackground="white",
                       padding=8)
        
        # Combobox
        style.configure("TCombobox", 
                       foreground=ThemeManager.COLORS["text"],
                       background="white")
                       
        # Status bar
        style.configure("Status.TLabel", 
                       background=ThemeManager.COLORS["secondary"],
                       foreground="white",
                       padding=3,
                       font=("Segoe UI", 9))
        
        # Main button
        style.configure("Main.TButton", 
                       font=("Segoe UI", 10, "bold"),
                       background=ThemeManager.COLORS["accent"],
                       foreground=ThemeManager.COLORS["link"],
                       padding=8)
        style.map("Main.TButton",
                 background=[("active", ThemeManager.COLORS["link"])],
                 relief=[("pressed", "sunken")])

def apply_text_styles(text_widget):
    text_widget.configure(
        font=("Segoe UI", 10),
        background="white",
        foreground=ThemeManager.COLORS["text"],
        selectbackground=ThemeManager.COLORS["accent"],
        selectforeground="white",
        padx=10,
        pady=10,
        borderwidth=1,
        relief="solid"
    )
    
    text_widget.tag_configure(
        "user", 
        foreground=ThemeManager.COLORS["primary"],
        font=("Segoe UI", 10, "bold"),
        lmargin1=10,
        lmargin2=20,
        background="#FFFACD"
    )
    
    text_widget.tag_configure(
        "assistant", 
        foreground=ThemeManager.COLORS["success"],
        font=("Segoe UI", 10),
        lmargin1=10,
        lmargin2=20
    )
    
    text_widget.tag_configure(
        "tool_header", 
        foreground=ThemeManager.COLORS["text_light"],
        font=("Segoe UI", 9, "italic"),
        background="#E6F3FF",
        lmargin1=10,
        lmargin2=10,
        rmargin=10
    )
    
    text_widget.tag_configure(
        "movie_title", 
        foreground=ThemeManager.COLORS["primary"],
        font=("Segoe UI", 12, "bold"),
        lmargin1=20,
        lmargin2=20,
        background="#E6F3FF"
    )
    
    text_widget.tag_configure(
        "info_label", 
        foreground=ThemeManager.COLORS["secondary"],
        font=("Segoe UI", 10, "bold"),
        lmargin1=25,
        lmargin2=25,
        background="#E6F3FF"
    )
    
    text_widget.tag_configure(
        "info_value", 
        foreground=ThemeManager.COLORS["text"],
        font=("Segoe UI", 10),
        lmargin1=25,
        lmargin2=120,
        background="#E6F3FF"
    )
    
    text_widget.tag_configure(
        "info_value_bold", 
        foreground=ThemeManager.COLORS["text"],
        font=("Segoe UI", 10, "bold"),
        lmargin1=25,
        lmargin2=120,
        background="#E6F3FF" 
    )
    
    text_widget.tag_configure(
        "results_header", 
        foreground=ThemeManager.COLORS["secondary"],
        font=("Segoe UI", 10, "bold"),
        lmargin1=20,
        lmargin2=20,
        background="#E6F3FF"
    )
    
    text_widget.tag_configure(
        "tool_section", 
        foreground=ThemeManager.COLORS["secondary"],
        font=("Segoe UI", 10, "bold"),
        lmargin1=20,
        lmargin2=20,
        background="#E6F3FF"
    )
    
    text_widget.tag_configure(
        "tool_item", 
        foreground=ThemeManager.COLORS["text"],
        font=("Segoe UI", 10, "bold"),
        lmargin1=20,
        lmargin2=30,
        background="#E6F3FF"
    )
    
    text_widget.tag_configure(
        "tool_detail", 
        foreground=ThemeManager.COLORS["text_light"],
        font=("Segoe UI", 9),
        lmargin1=30,
        lmargin2=40,
        background="#E6F3FF"
    )
    
    text_widget.tag_configure(
        "tool_link_label", 
        foreground=ThemeManager.COLORS["text"],
        font=("Segoe UI", 9),
        lmargin1=30,
        lmargin2=40,
        background="#E6F3FF"
    )
    
    text_widget.tag_configure(
        "tool_link", 
        foreground=ThemeManager.COLORS["link"],
        font=("Segoe UI", 9, "underline"),
        lmargin1=40,
        lmargin2=40,
        background="#E6F3FF"
    )
    
    text_widget.tag_configure(
        "tool_error", 
        foreground=ThemeManager.COLORS["error"],
        font=("Segoe UI", 9, "italic"),
        lmargin1=20,
        lmargin2=20,
        background="#E6F3FF"
    )