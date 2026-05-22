import requests
from bs4 import BeautifulSoup
import os

# Define the URLs we need to ingest
SUPPORT_URLS = {
    "HackerRank": "https://support.hackerrank.com/",
    "Claude": "https://support.claude.com/en/",
    "Visa": "https://www.visa.co.in/support.html"
}

# Define where to save the files relative to the project root
OUTPUT_DIR = "data/corpus"

def scrape_and_save(company_name, url):
    """Scrapes text from a URL and saves it to a text file."""
    # We use a standard User-Agent header to look like a normal web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    file_path = os.path.join(OUTPUT_DIR, f"{company_name.lower()}_support.txt")
    
    print(f"Attempting to scrape {company_name} from {url}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        
        # Parse the HTML and extract only the text
        soup = BeautifulSoup(response.text, 'html.parser')
        raw_text = soup.get_text(separator='\n', strip=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(raw_text)
            
        print(f"SUCCESS: Saved {company_name} data to {file_path}\n")
        
    except requests.exceptions.RequestException as e:
        print(f"FAILED: Could not scrape {company_name}. Error: {e}")
        print(f"Creating fallback mock data for {company_name} to keep the pipeline moving...\n")
        
        # Fallback text so you can keep building your AI agent even if blocked
        fallback_text = f"This is the official support documentation for {company_name}. If a user has an issue regarding {company_name} billing, accounts, or features, refer to these internal guidelines. Security issues must always be escalated."
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(fallback_text)

if __name__ == "__main__":
    print("--- Starting Knowledge Base Extraction ---\n")
    
    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for company, url in SUPPORT_URLS.items():
        scrape_and_save(company, url)
        
    print("--- Extraction Complete ---")