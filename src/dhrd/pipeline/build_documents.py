from pathlib import Path
import pandas as pd


def build_documents(
        tag_matrix: str, 
        foreign_key_file: str,
        foreign_key_name: str,
        output_dir: str
        ):
    """Builds documents.csv from tag matrix."""
    tags = pd.read_csv(Path(tag_matrix))
    documents = pd.DataFrame()

    # build documents ID
    documents['document_id'] = [f"DOC-{i:04d}" for i in range(1, len(tags)+1)]

    # extract foreign key
    fk = pd.read_csv(foreign_key_file)
    documents[foreign_key_name] = fk[foreign_key_name]
    
    # add columns from tag that can be taken as-is
    documents = documents.join(tags[['upload_date','download_id','title']])

    # generate download links
    documents['report_url'] = documents['download_id'].apply(lambda x: f"https://homicide-review.homeoffice.gov.uk/download/{x}")

    # reorder columns
    documents = documents[['document_id','incident_id','title','download_id','upload_date','report_url']]

    # store output
    documents.to_csv(Path(output_dir), index=False)