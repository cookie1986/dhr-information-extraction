# pdfs.py

import requests
from pathlib import Path
from utils.filesystem import set_output_directory

def download_pdf(download_id: str, output_path: Path):
    """Download a PDF file from the Home Office library using the provided download ID."""
    output_path = set_output_directory(output_path)

    download_url = f"https://homicide-review.homeoffice.gov.uk/download/{download_id}"
    try:
        response = requests.get(download_url, timeout=5)
        response.raise_for_status()
        # Check content type is pdf
        content_type = response.headers.get('Content-Type', '').lower()
        is_pdf = 'application/pdf' in content_type

        if is_pdf:
            filename = f"{download_id}.pdf"
            file_path = output_path / filename
            file_path.write_bytes(response.content)
    
    except requests.RequestException as e:
        print(f"Failed to download {download_id}: {e}")