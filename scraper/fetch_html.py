import requests
from pathlib import Path
from datetime import datetime

# # Note: this is a placeholder
# def create_metadata_file(base_url: str):
#     return {
#         "timestamp_utc": datetime.now.strftime("%Y-%m-%d %H:%M:%S"),
#         "base_url": base_url,
#         "pages_scraped": None, # empty for now until pagination is implemented
#         "html_files": [] # empty for now
#     }


def save_raw_html(html: str, output_dir: Path, filename: str):
    """Ensure the output directory exists and save the HTML content to a file"""
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / filename).write_text(html, encoding="utf-8")


def fetch_html_content(url, timeout: int = 3, page_count: int = 1, save_html: bool = True):
    """
    Fetch HTML content from the specified URL with pagination support.
    
    Args:
        url (str): The base URL to fetch HTML content from.
        timeout (int): The timeout for the HTTP request in seconds.
        page_count (int): The number of pages to fetch.
        save_html (bool): Whether to save the fetched HTML content to files.
        
    Returns:
        list: A list of HTML content for each fetched page.
    """

    html_content_list = []

    if save_html:
        output_dir = f"data/raw/html/{datetime.now()}"
    
    for page_num in range(page_count):
        # construct the page url
        page_url = f"{url}?pagination%5BpageNumber%5D={page_num}&pagination%5BpageSize%5D=100"
        
        try:
            response = requests.get(page_url, timeout=timeout)
            response.raise_for_status()
            # Append the HTML content to the global list
            html_content_list.append(response.text)
            
            if save_html:
                save_raw_html(response.text, output_dir=Path(output_dir), filename=f"html_response_page_{page_num}.html")
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    return html_content_list