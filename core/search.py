from duckduckgo_search import DDGS
from typing import Dict, Any, List

class SearchTool:
    def __init__(self, name: str):
        self.name = name
        
    def search(self, query: str) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement search method")

class DuckDuckGoSearch(SearchTool):
    def __init__(self):
        super().__init__("DuckDuckGo Search")
        
    def search(self, query: str) -> Dict[str, Any]:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("href", ""),
                    "snippet": result.get("body", "")
                })
                
            return {
                "tool": self.name,
                "query": query,
                "results": formatted_results
            }
        except Exception as e:
            return {
                "tool": self.name,
                "query": query,
                "error": str(e),
                "results": []
            }