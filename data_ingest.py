from src.fetch_results import fetch_html_content
from src.parse_fetch_results import parse_dhr_results, extract_data_from_section
from src.pagination import calculate_total_reports, calculate_total_pages

BASE = "https://homicide-review.homeoffice.gov.uk/"
PAGE_SIZE = 100

# Pagination testing
total_reports = calculate_total_reports(base_url=BASE)
print(f"total reports: {total_reports}")
total_pages = calculate_total_pages(total_reports, PAGE_SIZE)
print(f"total pages: {total_pages}")

# Fetch HTML content
html_content = fetch_html_content(url=BASE, page_count=total_pages, timeout=3, save_html=True)

# # Parse DHR results
# dhr_results = parse_dhr_results(html_content=html_content)

# # Extract data from DHR results sections
# structured_data_from_html = extract_data_from_section(dhr_results=dhr_results, output_dir="data/interim/", print_output=None)