# dev.py

from scraper.queries import extract_page_tags

extract_page_tags(
    url='https://homicide-review.homeoffice.gov.uk', 
    results_dir='data/raw/tags0/dhr_results.csv',
    keywords_dir='data/tagging_keywords.json'
    )