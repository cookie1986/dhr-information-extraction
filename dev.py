# dev.py

from scraper.queries import extract_page_tags

extract_page_tags(
    url='https://homicide-review.homeoffice.gov.uk', 
    results_dir='data/interim/dhr_results.csv',
    keywords_dir='utils/tagging_keywords.json'
    )