from bs4 import BeautifulSoup
from scraper.selectors import RESULTS_SELECTOR, DOWNLOAD_SELECTOR, TITLE_SELECTOR

def parse_dhr_reports(html_content_list: list):
    """Parse individual DHR reports from a list of HTML content strings"""
    dhr_results = []
    for html_content in html_content_list:
        soup = BeautifulSoup(html_content, 'html.parser')
        dhr_results.extend(soup.select(RESULTS_SELECTOR))

    return dhr_results

def parse_download_id(dhr_result: str):
    """Parse download ID from a DHR search result segment"""
    download_tag = dhr_result.select_one(DOWNLOAD_SELECTOR)['href'] if dhr_result.select_one(DOWNLOAD_SELECTOR) else None
    download_id = download_tag.split('/')[-1] if download_tag else "N/A"
    
    return download_id

def parse_title(dhr: str):
    """Parse title from a DHR search result segment"""
    title_element = dhr.select_one(TITLE_SELECTOR)
    title = " ".join(s.strip() for s in title_element.find_all(string=True, recursive=False) if s.strip()) if title_element else "N/A"

    return title