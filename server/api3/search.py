import json
import os
import requests
from bs4 import BeautifulSoup
from langchain_community.tools.bing_search import BingSearchResults
from langchain_community.utilities import BingSearchAPIWrapper
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

def extract_article_text(url):
    """
    Robust text extraction using requests and BeautifulSoup
    
    :param url: URL of the webpage
    :return: Extracted text or None if an error occurs
    """
    try:
        # Add headers to mimic browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch webpage with timeout and headers
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script, style, and navigation elements
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        
        # Extract text
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return ' '.join(lines)
    
    except requests.RequestException:
        return None  # Return None if a request error occurs
    except Exception:
        return None  # Return None for any other error

def perform_bing_search(api_key, query, num_results=5):
    """
    Perform Bing search with text extraction
    """
    try:
        # Create API wrapper
        api_wrapper = BingSearchAPIWrapper(
            bing_subscription_key=api_key,
            bing_search_url='https://api.bing.microsoft.com/v7.0/search',
            k=num_results
        )
        
        # Create Bing search tool
        tool = BingSearchResults(api_wrapper=api_wrapper)
        
        # Perform the search
        response = tool.invoke(query)
        
        # Parse the response
        results = json.loads(response.replace("'", '"'))
        
        # Extract full text for each result
        full_texts = []
        for result in results:
            link = result.get('link', '')
            full_text = extract_article_text(link)
            if full_text:  # Only add non-error results
                full_texts.append(full_text)
        
        return full_texts
    
    except Exception as e:
        return [f"Search Error: {str(e)}"]

def search_and_extract(query):
    """
    Perform Bing search and return raw extracted results
    
    :param query: Search query
    :return: List of extracted articles
    """
    # Get Bing API key from environment
    BING_API_KEY = os.getenv('BING_API_KEY')
    
    # Perform search and extract full texts
    full_texts = perform_bing_search(BING_API_KEY, query)
    
    return full_texts

def bing_search_engine(query):
    # Example usage
    results = search_and_extract(query)
    
    # Print results
    for idx, result in enumerate(results):
        print(f"Article {idx + 1}:\n{result}\n")
    return results

if __name__ == "__main__":
    bing_search_engine(query='Latest news about Palantir Technologies')
