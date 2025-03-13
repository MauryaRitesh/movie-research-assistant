import time
from typing import List, Dict, Any, Tuple, Optional
from core.search import SearchTool
from core.llm import LLMClient

class ConversationManager:
    def __init__(self, tools: List[SearchTool], llm: LLMClient):
        self.tools = {tool.name: tool for tool in tools}
        self.llm = llm
        self.history = []
    
    def add_message(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def add_tool_call(self, tool_name: str, query: str, results: Dict[str, Any]):
        self.history.append({
            "role": "tool",
            "tool": tool_name,
            "query": query,
            "results": results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def get_context_from_history(self) -> str:
        context_parts = []
        
        for entry in self.history:
            if entry["role"] == "tool" and "results" in entry:
                tool_results = entry["results"].get("results", [])
                if tool_results:
                    context_parts.append(f"Search results for '{entry['query']}' using {entry['tool']}:")
                    
                    for i, result in enumerate(tool_results, 1):
                        context_parts.append(
                            f"{i}. {result.get('title', '')}\n"
                            f"   {result.get('snippet', '')}\n"
                        )
        
        return "\n".join(context_parts)
    
    def process_query(self, query: str) -> Tuple[str, Dict[str, Any]]:
        self.add_message("user", query)
        
        search_tool = self.tools.get("DuckDuckGo Search")
        tool_results = {}
        
        if search_tool:
            search_results = search_tool.search(query)
            self.add_tool_call(search_tool.name, query, search_results)
            tool_results["search"] = search_results
        
        context = self.get_context_from_history()
        
        response = self.llm.generate_response(query, context)
        self.add_message("assistant", response)
        
        return response, tool_results