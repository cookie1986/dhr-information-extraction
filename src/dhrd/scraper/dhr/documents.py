# documents.py

import pandas as pd
from dhrd.scraper.download.pdfs import download_pdf

def download_pdfs(download_id_dir: str, output_dir: str):
    df = pd.read_csv(download_id_dir)
    download_ids = df['download_id'].tolist()
    for download_id in download_ids:
        download_pdf(
            download_id=download_id,
            output_path=output_dir
        )