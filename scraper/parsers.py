import math
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
from css_selectors import TOTAL_REPORTS_SELECTOR, RESULTS_SELECTOR, TITLE_SELECTOR, SUBSECTION_SELECTOR, DOWNLOAD_SELECTOR

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


def parse_dhr_reports(html_content_list: list):
    """Parse individual DHR reports from a list of HTML content strings"""
    dhr_results = []
    for html_content in html_content_list:
        soup = BeautifulSoup(html_content, 'html.parser')
        dhr_results.extend(soup.select(RESULTS_SELECTOR))

    return dhr_results


def extract_structured_data(dhr_results: list, output_dir: Path = "data/interim/"):
    """
    Extract data from DHR results sections and save to CSV
    
    Args:
        dhr_results (list): List of BeautifulSoup elements representing DHR results sections
        output_dir (Path, optional): Directory to save the extracted data CSV. Defaults to "data/interim/".
        print_output (str, optional): Level of detail to print during extraction. Options: 'verbose', 'title_only', None. Defaults to None.
        
        Returns:
            pd.DataFrame: DataFrame containing the extracted data
    """
    
    # Initialise empty dataframe to hold extracted data
    df = pd.DataFrame(columns=["title", "csp", "region", "upload_date", "death_date", "download_id"])
    
    # Loop through DHR result in HTML and extract relevant data
    for dhr in dhr_results:
    
        # Empty list to hold data extracted from HTML
        extracted_data = []

        # Extract title
        title_element = dhr.select_one(TITLE_SELECTOR)
        title = " ".join(s.strip() for s in title_element.find_all(string=True, recursive=False) if s.strip()) if title_element else "N/A"

        # Extract CSP, region, date of upload, date of death
        dhr_subsections = dhr.select(SUBSECTION_SELECTOR)
        csp = dhr_subsections[0].get_text().strip() if dhr_subsections else "N/A"

        csp_region = dhr_subsections[1].get_text().strip() if len(dhr_subsections) > 1 else "N/A"
        upload_date = dhr_subsections[2].get_text().strip() if len(dhr_subsections) > 2 else "N/A"
        death_date = dhr_subsections[3].get_text().strip() if len(dhr_subsections) > 3 else "N/A"

        # Extract the download ID
        download_tag = dhr.select_one(DOWNLOAD_SELECTOR)['href'] if dhr.select_one(DOWNLOAD_SELECTOR) else None
        download_id = download_tag.split('/')[-1] if download_tag else "N/A"

        # Append extracted data to list
        extracted_data.append({
            "title": title,
            "csp": csp,
            "region": csp_region,
            "upload_date": upload_date,
            "death_date": death_date,
            "download_id": download_id
        })

        # Add extracted data to dataframe
        df = pd.concat([df, pd.DataFrame(extracted_data)], ignore_index=True)
    
    # Write dataframe to CSV
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / "dhr_results.csv", index=False)

    return df