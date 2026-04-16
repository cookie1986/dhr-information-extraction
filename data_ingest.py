from src.fetch_results import fetch_html_content

# Fetch html content from Home Office library
url = "https://homicide-review.homeoffice.gov.uk/?pagination[pageNumber]=0"

html_content = fetch_html_content(url=url, timeout=3, save_html=True)