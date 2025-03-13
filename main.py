import tkinter as tk
from ui.app import RAGApp
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    root = tk.Tk()
    root.title("RAG Assistant")
    root.geometry("900x700")
    root.minsize(800, 600)
    
    app = RAGApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()