from pathlib import Path


def collect_local_files(root: Path) -> dict[str, Path]:
    """
    Return a mapping of repo-relative path -> absolute path for all files under `root`.
    """
    return {p.relative_to(root).as_posix(): p for p in root.rglob("*") if p.is_file()}

