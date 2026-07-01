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

def build_victims(
        tag_matrix: str,
        foreign_key_file: str,
        foreign_key_name: str,
        column_mapping_file: str,
        output_dir: str
        ):
    """Builds victims.csv from tag matrix."""
    tags = pd.read_csv(Path(tag_matrix))

    # join incident ID to tag matrix
    fk = pd.read_csv(foreign_key_file)
    tags = tags.join(fk[[foreign_key_name]])
    
    victims = pd.DataFrame()

    # filter tag matrix on incidents where number of victims equals 1 (TEMPORARY FILTERING STEP)
    single_victim_tags = tags[
        tags['Victim-Specific Information.Number of victims in the DHR[]_2'
             ] == False].copy().reset_index(drop=True)
    
    # build victim ID
    victims['victim_id'] = [f"VIC-{i:04d}" for i in range(1, len(single_victim_tags)+1)]

    # add incident ID
    victims[foreign_key_name] = single_victim_tags[foreign_key_name]

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
            victims[output_col] = single_victim_tags[raw_cols[0]]

        else:
            value_map = col.get("value_map")

            if value_map is None:
                value_map = {
                    raw_col: tidy_label(raw_col)
                    for raw_col in raw_cols
                }

            selected = single_victim_tags[raw_cols].idxmax(axis=1).map(value_map)
            has_value = single_victim_tags[raw_cols].any(axis=1)

            victims[output_col] = selected.where(has_value)

            # populate missing values with 'missing' flag
            victims[output_col] = victims[output_col].fillna('Unknown')

    # write to csv
    victims.to_csv(output_dir, index=False)