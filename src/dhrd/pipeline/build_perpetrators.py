import pandas as pd
from pathlib import Path
import json

def tidy_label(raw_col):
    return (
        raw_col
        .split("[]_")[-1]
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("-", "_")
    )

def build_perpetrators(
        tag_matrix: str,
        foreign_key_file: str,
        foreign_key_name: str,
        column_mapping_file: str,
        output_dir: str
        ):
    """Builds perpetrators.csv from tag matrix."""
    tags = pd.read_csv(Path(tag_matrix))

    # join incident ID to tag matrix
    fk = pd.read_csv(foreign_key_file)
    tags = tags.join(fk[[foreign_key_name]])
    
    perpetrators = pd.DataFrame()

    # # filter tag matrix on incidents where number of perpetrators equals 1 (TEMPORARY FILTERING STEP)
    # single_perpetrators_tags = tags[
    #     tags['Victim-Specific Information.Number of victims in the DHR[]_2'
    #          ] == False].copy().reset_index(drop=True)
    
    # build perpetrator ID
    perpetrators['perpetrator_id'] = [f"SUS-{i:04d}" for i in range(1, len(tags)+1)]

    # add incident ID
    perpetrators[foreign_key_name] = tags[foreign_key_name]

    # load column mapping file
    try:
        with open(column_mapping_file, 'r') as f:
            column_map = json.load(f)
    except Exception as e:
        print(f"Error loading column mapping: {e}")
    
    
    for col in column_map:
        raw_cols = col["raw_cols"]
        output_col = col["argmax_col"]

        if len(raw_cols) == 1:
            perpetrators[output_col] = tags[raw_cols[0]]

        else:
            value_map = col.get("value_map")

            if value_map is None:
                value_map = {
                    raw_col: tidy_label(raw_col)
                    for raw_col in raw_cols
                }

            selected = tags[raw_cols].idxmax(axis=1).map(value_map)
            has_value = tags[raw_cols].any(axis=1)

            perpetrators[output_col] = selected.where(has_value)

            # populate missing values with 'missing' flag
            perpetrators[output_col] = perpetrators[output_col].fillna('Unknown')

    # write to csv
    perpetrators.to_csv(output_dir, index=False)