import os

def is_typeshed_file(typeshed_dir: str | None, file: str) -> bool:
    typeshed_dir = typeshed_dir if typeshed_dir is not None else TYPESHED_DIR
    try:
        return os.path.commonpath((typeshed_dir, os.path.abspath(file))) == typeshed_dir
    except ValueError:  # Different drives on Windows
        return False

