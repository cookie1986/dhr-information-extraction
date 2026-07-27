# src/dhrd/versioning.py

from pathlib import Path

VERSION_FILE = Path(__file__).resolve().parents[2] / "dataset_versioning.txt"

def get_version() -> str:
    return VERSION_FILE.read_text().strip()

def next_version(part: str) -> str:
    major, minor, patch = map(int, get_version().split("."))

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        major = major
        minor += 1
        patch = 0
    elif part == "patch":
        major = major
        minor = minor
        patch += 1
    else:
        AttributeError('part must be one of: "major", "minor", or "patch"')

    return f"{major}.{minor}.{patch}"

def set_version(version: str) -> None:
    VERSION_FILE.write_text(version + "\n")