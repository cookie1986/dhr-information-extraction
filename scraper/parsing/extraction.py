from pathlib import Path
import pandas as pd
from scraper.selectors import SUBSECTION_SELECTOR
from scraper.parsing.reports import parse_download_id, parse_title

def extract_report_data(dhr_results: list, output_dir: Path = "data/raw/tags/"):
    """
    Extract data from DHR results sections and save to CSV
    
    Args:
        dhr_results (list): List of html strings representing DHR results sections
        output_dir (Path): Directory to save the extracted data CSV. Defaults to "data/raw/tags/".
        
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
        title = parse_title(dhr)

        # Extract CSP, region, date of upload, date of death
        dhr_subsections = dhr.select(SUBSECTION_SELECTOR)

        # Append extracted data to list
        extracted_data.append({
            "title": title,
            "csp": dhr_subsections[0].get_text().strip() if dhr_subsections else "N/A",
            "region": dhr_subsections[1].get_text().strip() if len(dhr_subsections) > 1 else "N/A",
            "upload_date": dhr_subsections[2].get_text().strip() if len(dhr_subsections) > 2 else "N/A",
            "death_date": dhr_subsections[3].get_text().strip() if len(dhr_subsections) > 3 else "N/A",
            "download_id": parse_download_id(dhr)
        })

        # Add extracted data to dataframe
        df = pd.concat([df, pd.DataFrame(extracted_data)], ignore_index=True)
    
    # Write dataframe to CSV
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / "dhr_results.csv", index=False)

    return df