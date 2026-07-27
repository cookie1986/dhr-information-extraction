# src/dhrd/release/package.py

from pathlib import Path
import zipfile
import shutil
from dhrd.versioning import next_version

PROCESSED_DIR = Path("data/processed")
RELEASES_DIR = Path("releases")
RELEASE_ASSETS_DIR = Path("release_assets")

def package_release(part: str) -> str:
    version = next_version(part)

    release_dir = RELEASES_DIR / version

    if release_dir.exists():
        raise FileExistsError(
            f"Release directory already exists for {release_dir}"
        )

    release_dir.mkdir(parents=True)

    for file in PROCESSED_DIR.glob("*.csv"):
        shutil.copy2(file, release_dir / file.name)

    for item in RELEASE_ASSETS_DIR.iterdir():
        destination = release_dir / item.name

        if item.is_dir():
            shutil.copytree(item, destination)
        else:
            shutil.copy2(item, destination)

    with zipfile.ZipFile(
        release_dir / f"dhr-data-release-v{version}.zip", mode="w",
        compression=zipfile.ZIP_DEFLATED
        ) as zf:
        [zf.write(file) for file in RELEASE_ASSETS_DIR.iterdir()]

    print(f"Packaged dataset release {version}")

    return version