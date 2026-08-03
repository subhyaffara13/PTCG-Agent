from pathlib import Path


def _is_package(path: Path) -> bool:
    return exists_case_sensitive(str(path)) and path.is_dir()

