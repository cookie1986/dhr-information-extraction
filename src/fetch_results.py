import requests
from pathlib import Path
from datetime import datetime

# Note: this is a placeholder
def create_metadata_file(base_url: str):
    return {
        "timestamp_utc": datetime.now.strftime("%Y-%m-%d %H:%M:%S"),
        "base_url": base_url,
        "pages_scraped": None, # empty for now until pagination is implemented
        "html_files": [] # empty for now
    }


def save_raw_html(html: str, output_dir: Path, filename: str):
    # Ensure the output directory exists and save the HTML content to a file
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / filename).write_text(html, encoding="utf-8")


def fetch_html_content(url, timeout: int = 3, save_html: bool = True):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        if save_html:
            save_raw_html(response.text, output_dir=Path("data/raw/html/"), filename="home_office_library.html")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None