from pathlib import Path

def check_file_exists(file_dir: str):
    """Check whether a file exists in a specified directory."""
    file_path = Path(file_dir)
    if file_path.is_file():
        return True
    else:
        raise FileNotFoundError(f"Results file not found for: {file_dir}")