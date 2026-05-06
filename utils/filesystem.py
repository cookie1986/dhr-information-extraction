# filesystem.py

from pathlib import Path

def check_file_exists(file_dir: str):
    """Check whether a local file exists in a specified directory."""
    file_path = Path(file_dir)
    if file_path.is_file():
        return True
    else:
        raise FileNotFoundError(f"Results file not found for: {file_dir}")
    
def set_output_directory(output_dir: str) -> Path:
    """Set an output directory."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path