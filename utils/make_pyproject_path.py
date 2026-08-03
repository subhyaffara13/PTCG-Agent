import os

def make_pyproject_path(unpacked_source_directory: str) -> str:
    return os.path.join(unpacked_source_directory, "pyproject.toml")

