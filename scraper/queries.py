"""
queries.py

High-level queries for fetching and processing DHR reports from the Home Office website.
"""
import json
import pandas as pd
from scraper.client import fetch_html
from scraper.parsers import count_total_reports, calculate_total_pages, parse_dhr_reports, extract_structured_data, parse_download_id
from utils.filesystem import check_file_exists


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


def extract_page_tags(url: str, results_dir: str, keywords_dir: str):
    # Check if results file already exists
    if check_file_exists(results_dir):
        results_data = pd.read_csv(results_dir)
        
        # Load keywords file
        with open(keywords_dir, 'r') as f:
            keywords_json = json.load(f)
        keywords = [k for k in keywords_json['keywords']]
        
        # Call first page of each keyworded url
        for k in keywords:
            pages = []
            params = {
                "pagination[pageNumber]": 0,
                "pagination[pageSize]": 100,
                "internal.dhr-category[]": k
                }
            pages.append(fetch_html(url=url, timeout=3, params=params))
            
            # Calculate total reports under keyword - pagination support
            total_reports_in_query = count_total_reports(pages[0])
            
            if total_reports_in_query < 1:
                # A known bug caused by 'showing results' section of count_total_reports -- this should be a hacky workaround for now
                total_pages_in_query = 1
            else:
                # Calculate total pages to iterate over
                total_pages_in_query = calculate_total_pages(total_reports=total_reports_in_query)
            
            # Iterate over remaining pages and append to list
            for page_num in range(1, total_pages_in_query):
                # Update params with new page number
                params['pagination[pageNumber]'] = page_num
                # Fetch HTML and add to list
                pages.append(fetch_html(url=url, timeout=3, params=params))
            
            # Parse DHR reports from page content
            dhr_query_results = parse_dhr_reports(html_content_list=pages)
            
            # Extract the download IDs
            download_ids = [parse_download_id(dhr) for dhr in dhr_query_results]

            # Cross ref with results page and mark 'Y' if download ID present, 'N' otherwise
            results_data[k] = results_data['download_id'].isin(download_ids).map({True: "True", False: "False"})
        
        # Write the updated file to CSV
        results_data.to_csv('data/interim/dhr_results_updated_tags.csv', index=False)
