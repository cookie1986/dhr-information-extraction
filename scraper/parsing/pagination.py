import math
from bs4 import BeautifulSoup
from scraper.selectors import TOTAL_REPORTS_SELECTOR

def count_total_reports(html_content: str) -> int:
    """Count the total number of reports from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    total_results_caption = soup.select(TOTAL_REPORTS_SELECTOR)
    for element in total_results_caption:
        if element.get_text(strip=True).startswith("Showing results"):
            total_results = element.get_text(strip=True)
            return int(total_results.split()[-1])
    return 0

def calculate_total_pages(total_reports: int, page_size: int = 100) -> int:
    """Calculate the total number of pages to iterate over based on the total number of reports and the max page size."""
    return math.ceil(total_reports / page_size)

def build_query_params(filter_param_key, filter_param_val, page_number = 0, page_size=100):
    # Set base params
    params = {
        "pagination[pageNumber]": page_number,
        "pagination[pageSize]": page_size
    }
    # Append selected filter to params
    params[filter_param_key] = filter_param_val

    return params