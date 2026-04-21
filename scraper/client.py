import requests
from typing import Optional

def fetch_html(url: str, timeout: int = 3, params: Optional[dict] = None) -> str:
    """Fetch HTML content from the specified URL with optional query parameters."""
    try:
        response = requests.get(url, timeout=timeout, params=params)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None