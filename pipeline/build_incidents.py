from pathlib import Path
import pandas as pd
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


def build_incidents(tag_matrix: str, col_mapping_file: str, output_dir: str):
    """Builds incidents.csv from tag matrix."""
    tags = pd.read_csv(Path(tag_matrix))
    incidents = pd.DataFrame()

    # build incident ID
    incidents['incident_id'] = [f"INC-{i:04d}" for i in range(1, len(tags)+1)]

    # load in single column mappings
    try:
        column_mapping = Path(col_mapping_file)
        with open(column_mapping, 'r') as f:
            column_map = json.load(f)
    except Exception as e:
        print(f"Error loading dummy_mapping: {e}")

    for col in column_map:
        raw_cols = col["raw_cols"]
        output_col = col["argmax_col"]

        if len(raw_cols) == 1:
            incidents[output_col] = tags[raw_cols[0]]

        else:
            value_map = col.get("value_map")

            if value_map is None:
                value_map = {
                    raw_col: tidy_label(raw_col)
                    for raw_col in raw_cols
                }

            selected = tags[raw_cols].idxmax(axis=1).map(value_map)
            has_value = tags[raw_cols].any(axis=1)

            incidents[output_col] = selected.where(has_value)

   
    # for col in column_map:
    #     raw_cols = col["raw_cols"]
    #     output_col = col["argmax_col"]

    #     if len(raw_cols) == 1:
    #         incidents[output_col] = tags[raw_cols[0]]

    #     else:
    #         # Clean names from the raw column names
    #         value_map = {
    #             raw_col: raw_col.split("[]_")[-1]
    #             for raw_col in raw_cols
    #         }

    #         # Find the first TRUE column per row
    #         incidents[output_col] = (
    #             tags[raw_cols]
    #             .idxmax(axis=1)
    #             .map(value_map)
    #         )

    # store output
    incidents.to_csv(Path(output_dir), index=False)