import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

import requests

print("Agentic QA starting...")

def main():
    query = "What is the weather in Cyberjaya right now?"
    print(f"Question: {query}")
    result = answer_question(query)
    print("\nResult:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
def answer_question(query: str) -> Dict[str, Any]:
    start_time = time.time()
    
    #This is where the agent logic will live
    
    end_time = time.time()
    duration_ms = round((end_time - start_time)*1000)
    
    return {
        "answer": "not yet implementd",
        "sources": [],
        "latency_ms":{
            "total": duration_ms,
            "by_step": {}
        }
    }
    
def ddg_search(query: str) -> dict:
    """Call DuckuckGo Instant Answer API - lightweight, no key needed"""
    t0 = time.time()
    
    url = "https://api.duckduckgo.com/"
    params ={
        "q": query,
        "format": "json",
        "pretty": "1",
        "no_html": 1, # remove html tags
        "skip_disambig": 1, #avoid redirect pages
        "no_redirect": 1
    }
    
    try:
        response = response.get(url, params=params, timeout=6)    # Sends an HTTP GET request to url, attaches a qeury parameters, waits at most 6 seconds for a response, return a Response object
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()       # Parses the HTTP response body as JSON
        
        main_answer = ""
        main_url = ""
        
        if data.get("Abstract"):
            main_answer = data["Abstract"]
            main_url = data.get("AbstractURL", "")
            
        elif data.get("Answer"):
            main_answer = data["Answer"]
            main_url = data.get("AnswerURL", "")
            
        elif data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
            topic = data["RelatedTopics"][0]
            if "Text" in topic:
                main_answer = topic["Text"].strip()
            if "FirstURL" in topic:
                main_url = topic["FirstURL"]
                
        result = {
            "query": query,
            "text": main_answer or "(no clear answer found)",
            "url": main_url or "(no source url)",
            "more_results_count": len(data.get("RelatedTopics", [])),
            "infobox": data.get("Infobox", {}) is not None
        }
        
    except requests.Timeout:
        result = {"error": "Request timed out", "query": query}
    except requests.RequestException as e:
        result = {"error": str(e), "query": query}
    except Exception as e:
        result = {"error": f"An unexpected error occurred: {str(e)}", "query": query}
        
    duration_ms = round((time.time() - t0)*1000)
    print(f"DDG Search completed in {duration_ms} ms")
    
    return result
        
                
            
            
    
if __name__ == "__main__":
    main()
    
    