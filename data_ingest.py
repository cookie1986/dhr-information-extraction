from src.fetch_results import fetch_html_content
from src.parse_fetch_results import parse_dhr_results, extract_data_from_section
from src.pagination import calculate_total_reports, calculate_total_pages

BASE = "https://homicide-review.homeoffice.gov.uk/"
PAGE_SIZE = 100

# Pagination testing
total_reports = calculate_total_reports(base_url=BASE)
total_pages = calculate_total_pages(total_reports, PAGE_SIZE)

# Fetch HTML content (returns list of html content for each page)
html_content_list = fetch_html_content(url=BASE, page_count=total_pages, timeout=3, save_html=True)

# Parse DHR results (returns list)
dhr_results = parse_dhr_results(html_content_list=html_content_list)

# # Extract data from DHR results sections
structured_data_from_html = extract_data_from_section(dhr_results=dhr_results, output_dir="data/interim/", print_output=None)