# test_download.py

from unittest.mock import patch
from dhrd.scraper.download.pdfs import download_pdf

@patch('scraper.download.pdfs.requests.get')
def test_download_pdf(mock_get, tmp_path):
    """Test download_pdf function with a mocked requests.get."""
    
    # Mock HTTP request and response
    mock_get.return_value.status_code = 200
    mock_get.return_value.headers = {'Content-Type': 'application/pdf'}
    mock_get.return_value.content = b'Fake PDF data'
    
    # Set output directory
    output_dir = tmp_path
    # Call PDF download function with a tets download ID
    download_pdf("123", output_dir)
    # Set output file path
    output_file = output_dir / "123.pdf"
    
    # Check file exists and content is correct
    assert output_file.exists()
    assert output_file.read_bytes() == b'Fake PDF data'
