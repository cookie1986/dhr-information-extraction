# test_client.py

from unittest.mock import patch
from dhrd.scraper.client import get_html

@patch('scraper.client.requests.get')
def test_get_html(mock_get):
    """Test get_html function with a mocked requests.get."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html></html>"
    result = get_html("http://example.com")

    assert "<html" in result