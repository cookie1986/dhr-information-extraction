"""
selectors.py

Central store for CSS selectors used in the scraper and parser modules.
"""

results_selector = "section[aria-label^='DHR result']"
subsection_selector = ".govuk-grid-row.govuk-\!-padding-top-2 .govuk-grid-column-one-quarter .govuk-label.dhrr-results-card--detail-value"
title_selector = "h3.govuk-heading-s"
download_selector = ".govuk-grid-row.govuk-\!-padding-top-2 .govuk-grid-column-full .govuk-button-group.govuk-\!-margin-0 a[href^='/download/']"
TOTAL_REPORTS_SELECTOR = ".govuk-grid-column-two-thirds .govuk-grid-row .govuk-grid-column-full .govuk-caption-m"