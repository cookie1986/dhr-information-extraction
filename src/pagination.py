import math
import requests
from bs4 import BeautifulSoup

# CSS selectors
showing_results_selector = ".govuk-grid-column-two-thirds .govuk-grid-row .govuk-grid-column-full .govuk-caption-m"


def calculate_total_reports(base_url: str, timeout: int = 3) -> int:
     """
     Calculate the total number of DHRs on the Home Office library.

     returns:
            int: Total number of DHRs
     """
     # call the base URL and parse the HTML content
     response = requests.get(base_url, timeout=timeout)
     response.raise_for_status()
     html_content = BeautifulSoup(response.text, "html.parser")

     total_results_caption = html_content.select(showing_results_selector)
     for i, element in enumerate(total_results_caption):
         if total_results_caption[i].get_text(strip=True).startswith("Showing results"):
             total_results = total_results_caption[i].get_text(strip=True)
             
             return int(total_results.split()[-1])
         

def calculate_total_pages(total_reports: int, page_size: 100) -> int:
    """Calculate the total number of pages based on the total number of reports and page size."""
    return math.ceil(total_reports / page_size)