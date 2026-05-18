from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()
from rich import print

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Perform search on the web and return the top results.Returns Title, URL,& Snippets"""
    result = tavily.search(query=query,max_results=3)

    out = []
    for r in result['results']:
        out.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n")
    return "\n------\n".join(out)

#print(web_search.invoke("What is the capital of Odisha?"))

@tool
def scrap_url(url:str) ->str:
    """Scrap & return clean text content from a given url for deeper reading"""
    try:
        resp = requests.get(url,timeout=8,headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, 'html.parser')
        for tag in soup(['script', 'style','nav','footer','header','aside']):
            tag.decompose()
        return soup.get_text(separator='\n', strip=True)[:3000]
    except Exception as e:
        return f"could not fetch content from url: {e}"
    
T=scrap_url.invoke("https://en.wikipedia.org/wiki/Joda")    
#print(T)

