# src/dhrd/build.py

from dhrd.pipeline.build_incidents import build_incidents
from dhrd.pipeline.build_documents import build_documents
from dhrd.pipeline.build_victims import build_victims
from dhrd.pipeline.build_perpetrators import build_perpetrators

TAG_MATRIX = 'data/raw/tags/dhr_tag_matrix.csv'
INCIDENTS_OUT = 'data/processed/incidents.csv'
DOCUMENTS_OUT = 'data/processed/documents.csv'
VICTIMS_OUT = 'data/processed/victims.csv'
PERPETRATORS_OUT = 'data/processed/perpetrators.csv'
INCIDENT_COLUMN_MAPPING = 'data/resources/incident_column_mapping.json'
VICTIM_COLUMN_MAPPING = 'data/resources/victim_column_mapping.json'
PERPETRATOR_COLUMN_MAPPING = 'data/resources/perpetrator_column_mapping.json'

def build_all() -> None:
    build_incidents(
        tag_matrix=TAG_MATRIX,
        col_mapping_file= INCIDENT_COLUMN_MAPPING,
        output_dir = INCIDENTS_OUT
    )
    build_documents(
        tag_matrix = TAG_MATRIX,
        foreign_key_name = 'incident_id',
        foreign_key_file = INCIDENTS_OUT,
        output_dir = DOCUMENTS_OUT
    )
    build_victims(
        tag_matrix=TAG_MATRIX,
        foreign_key_name = 'incident_id',
        foreign_key_file = INCIDENTS_OUT,
        column_mapping_file = VICTIM_COLUMN_MAPPING,
        output_dir = VICTIMS_OUT
    )
    build_perpetrators(
        tag_matrix=TAG_MATRIX,
        foreign_key_name = 'incident_id',
        foreign_key_file = INCIDENTS_OUT,
        column_mapping_file = PERPETRATOR_COLUMN_MAPPING,
        output_dir = PERPETRATORS_OUT
    )