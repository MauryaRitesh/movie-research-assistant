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
                    
                    if entry["tool"] == "DuckDuckGo Search":
                        for i, result in enumerate(tool_results, 1):
                            context_parts.append(
                                f"{i}. {result.get('title', '')}\n"
                                f"   {result.get('snippet', '')}\n"
                            )
                    elif entry["tool"] == "OMDB Search":
                        for i, result in enumerate(tool_results, 1):
                            context_parts.append(
                                f"{i}. {result.get('title', '')} ({result.get('year', '')})\n"
                                f"   IMDB Rating: {result.get('rating', 'N/A')}\n"
                                f"   Genre: {result.get('genre', '')}\n"
                                f"   Director: {result.get('director', '')}\n"
                                f"   Actors: {result.get('actors', '')}\n"
                                f"   Plot: {result.get('plot', '')}\n"
                                f"   IMDB: {result.get('imdbLink', '')}\n"
                            )
                    elif entry["tool"] == "YouTube Search":
                        for i, result in enumerate(tool_results, 1):
                            context_parts.append(
                                f"{i}. {result.get('title', '')}\n"
                                f"   {result.get('description', '')}\n"
                                f"   Link: {result.get('link', '')}\n"
                            )
        
        return "\n".join(context_parts)
    
    def process_query(self, query: str) -> Tuple[str, Dict[str, Any]]:
        self.add_message("user", query)
        
        tool_results = {}
        
        self.add_message("assistant", f"Calling DuckDuckGo search: {query}")
        
        search_tool = self.tools.get("DuckDuckGo Search")
        if search_tool:
            imdb_query = f"{query} imdb rating release date director starring"
            search_results = search_tool.search(imdb_query)
            self.add_tool_call(search_tool.name, imdb_query, search_results)
            tool_results["search"] = search_results
        
        self.add_message("assistant", f"Calling YouTube search: {query}")
        
        youtube_tool = self.tools.get("YouTube Search")
        if youtube_tool:
            trailer_query = f"{query} trailer"
            youtube_results = youtube_tool.search(trailer_query)
            
            if youtube_results.get("results") and len(youtube_results["results"]) > 1:
                youtube_results["results"] = [youtube_results["results"][0]]
                
            self.add_tool_call(youtube_tool.name, trailer_query, youtube_results)
            tool_results["youtube"] = youtube_results
        
        if youtube_tool and youtube_results.get("results"):
            trailer_info = youtube_results["results"][0]
            trailer_message = f"Found Trailer for {query}: {trailer_info.get('link', '')}"
            self.add_message("assistant", trailer_message)
        
        context = self.get_context_from_history()
        
        response = self.llm.generate_response(query, context)
        self.add_message("assistant", response)
        
        return response, tool_results