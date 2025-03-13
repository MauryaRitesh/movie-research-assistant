from duckduckgo_search import DDGS
from typing import Dict, Any, List
import requests
import os
import googleapiclient.discovery

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
                if "imdb" not in query.lower():
                    search_query = f"{query} IMDB"
                else:
                    search_query = query
                    
                results = list(ddgs.text(search_query, max_results=2)) #setting search results =2 for now.
                
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

class OMDBSearch(SearchTool):
    def __init__(self):
        super().__init__("OMDB Search")
        self.api_key = os.getenv("OMDB_API_KEY")
        if not self.api_key:
            raise ValueError("OMDB API Key must be set in environment variables")
        self.base_url = "http://www.omdbapi.com/"
        
    def search(self, query: str) -> Dict[str, Any]:
        try:
            search_terms = query.lower()
            if "movie" in search_terms or "film" in search_terms or "series" in search_terms:
                search_terms = search_terms.replace("movie", "").replace("film", "").replace("series", "").strip()
            
            params = {
                "apikey": self.api_key,
                "s": search_terms
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            formatted_results = []
            
            if data.get("Response") == "True" and "Search" in data:
                search_results = data["Search"][:3]
                
                for item in search_results:
                    detail_params = {
                        "apikey": self.api_key,
                        "i": item["imdbID"]
                    }
                    
                    detail_response = requests.get(self.base_url, params=detail_params)
                    detail_data = detail_response.json()
                    
                    if detail_data.get("Response") == "True":
                        formatted_results.append({
                            "title": detail_data.get("Title", ""),
                            "year": detail_data.get("Year", ""),
                            "rating": detail_data.get("imdbRating", "N/A"),
                            "plot": detail_data.get("Plot", ""),
                            "director": detail_data.get("Director", ""),
                            "actors": detail_data.get("Actors", ""),
                            "genre": detail_data.get("Genre", ""),
                            "poster": detail_data.get("Poster", ""),
                            "imdbLink": f"https://www.imdb.com/title/{detail_data.get('imdbID', '')}"
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

class YouTubeSearch(SearchTool):
    def __init__(self):
        super().__init__("YouTube Search")
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YouTube API Key must be set in environment variables")
            
        self.youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=self.api_key
        )
        
    def search(self, query: str) -> Dict[str, Any]:
        try:
            # Always search for trailers
            search_terms = query.lower()
            if "trailer" not in search_terms:
                search_terms += " official trailer"
                
            # Add "movie" or "tv show" if not present to improve results
            if "movie" not in search_terms and "tv" not in search_terms and "show" not in search_terms:
                search_terms += " movie"
            
            search_response = self.youtube.search().list(
                q=search_terms,
                part="snippet",
                maxResults=1,  # Only get the top result
                type="video"
            ).execute()
            
            formatted_results = []
            
            for item in search_response.get("items", []):
                video_id = item["id"]["videoId"]
                formatted_results.append({
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                    "link": f"https://www.youtube.com/watch?v={video_id}",
                    "videoId": video_id
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