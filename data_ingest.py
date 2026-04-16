from src.fetch_results import fetch_html_content
from src.parse_fetch_results import parse_dhr_results, extract_data_from_section

# Fetch html content from Home Office library
url = "https://homicide-review.homeoffice.gov.uk/?pagination[pageNumber]=0"

# Fetch HTML content
html_content = fetch_html_content(url=url, timeout=3, save_html=True)

# Parse DHR results
dhr_results = parse_dhr_results(html_content=html_content)

# Extract data from DHR results sections
structured_data_from_html = extract_data_from_section(dhr_results=dhr_results, output_dir="data/interim/", print_output=None)