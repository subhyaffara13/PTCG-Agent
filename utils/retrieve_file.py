import time
from pathlib import Path


def retrieve_file(url: str, download_dir: Path = DOWNLOAD_DIR, wait: float = 5) -> Path:
    path = output_file(url, download_dir)
    if path.exists():
        print(f"Skipping {url} (already exists: {path})")
    else:
        download_dir.mkdir(exist_ok=True, parents=True)
        print(f"Downloading {url} to {path}")
        try:
            download(url, path)
        except HTTPError:
            time.sleep(wait)  # wait a few seconds and try again.
            download(url, path)
    return path

