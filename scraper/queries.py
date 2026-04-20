"""
queries.py

High-level queries for fetching and processing DHR reports from the Home Office website.
"""
from client import fetch_html
from parsers import count_total_reports, calculate_total_pages, parse_dhr_reports, extract_structured_data


def extract_page_data(url: str, timeout: int = 3, results_dir: str = "data/interim/"):
    """
    High-level function to extract data from DHR reports.
    
    Steps:
    1. Fetch HTML content from the first page of the DHR library.
    2. Parse the HTML content to support pagination.
    3. Extract structured data from the DHR results sections.
    4. Iterate over remaining pages
    5. Save the extracted data to CSV
    """

    PAGE_SIZE = 100

    # Empty list to store HTML content for all pages
    pages = []

    # Fetch HTML content from the first page
    pages.append(fetch_html(url=url, timeout=timeout, params={"pagination[pageSize]": PAGE_SIZE}))
    
    # Count the total number of reports from the first page of the HTML content
    total_reports = count_total_reports(html_content=pages[0])

    # Calculate the total pages within the query
    total_pages = calculate_total_pages(total_reports=total_reports)

    # Fetch the remaining pages and append to the pages list
    for page_num in range(1, total_pages):
        pages.append(fetch_html(url=url, timeout=timeout, params={"pagination[pageNumber]": page_num, "pagination[pageSize]": PAGE_SIZE}))
    
    # Parse the HTML page content to extract individual DHR reports
    dhr_results = parse_dhr_reports(html_content_list=pages)

    # Extract the structured page data from each DHR and save as CSV
    extract_structured_data(dhr_results=dhr_results, output_dir=results_dir)


