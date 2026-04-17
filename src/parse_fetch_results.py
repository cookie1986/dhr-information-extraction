from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup

# CSS selectors for parsing DHR results page
results_selector = "section[aria-label^='DHR result']"
subsection_selector = ".govuk-grid-row.govuk-\!-padding-top-2 .govuk-grid-column-one-quarter .govuk-label.dhrr-results-card--detail-value"
title_selector = "h3.govuk-heading-s"
download_selector = ".govuk-grid-row.govuk-\!-padding-top-2 .govuk-grid-column-full .govuk-button-group.govuk-\!-margin-0 a[href^='/download/']"

# Function to parse DHR results page
def parse_dhr_results(html_content_list: list):
    dhr_results = []
    for html_content in html_content_list:
        soup = BeautifulSoup(html_content, 'html.parser')
        dhr_results.extend(soup.select(results_selector))

    return dhr_results


# Function to extract data from DHR results sections
def extract_data_from_section(dhr_results: list, output_dir: Path = "data/interim/", print_output: str = None):
    
    # Initialise empty dataframe to hold extracted data
    df = pd.DataFrame(columns=["title", "csp", "region", "upload_date", "death_date", "download_id"])
    
    # Loop through DHR result in HTML and extract relevant data
    
    for dhr in dhr_results:
    
        # Empty list to hold data extracted from HTML
        extracted_data = []

        # Extract title
        title_element = dhr.select_one(title_selector)
        title = " ".join(s.strip() for s in title_element.find_all(string=True, recursive=False) if s.strip()) if title_element else "N/A"

        # Extract CSP, region, date of upload, date of death
        dhr_subsections = dhr.select(subsection_selector)
        csp = dhr_subsections[0].get_text().strip() if dhr_subsections else "N/A"

        csp_region = dhr_subsections[1].get_text().strip() if len(dhr_subsections) > 1 else "N/A"
        upload_date = dhr_subsections[2].get_text().strip() if len(dhr_subsections) > 2 else "N/A"
        death_date = dhr_subsections[3].get_text().strip() if len(dhr_subsections) > 3 else "N/A"

        # Extract the download ID
        download_tag = dhr.select_one(download_selector)['href'] if dhr.select_one(download_selector) else None
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

        # Auditing
        if print_output == 'verbose':
            print(f"Title: {title}")
            print(f"Community Service Partnership: {csp}")
            print(f"Region: {csp_region}")
            print(f"Upload Date: {upload_date}")
            print(f"Death Date: {death_date}")
            print(f"Download ID: {download_id}")
            print("-------end of section-------")
        elif print_output == 'title_only':
            print(f"Title: {title}")
        else:
            pass

        # Add extracted data to dataframe
        df = pd.concat([df, pd.DataFrame(extracted_data)], ignore_index=True)
    
    # Write dataframe to CSV
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / "dhr_results.csv", index=False)

    return df