import re
from pathlib import Path


def output_file(url: str, download_dir: Path = DOWNLOAD_DIR) -> Path:
    file_name = url.strip()
    for part in NAME_REMOVE:
        file_name = file_name.replace(part, '').strip().strip('/:').strip()
    return Path(download_dir, re.sub(r"[^\-_\.\w\d]+", "_", file_name))

