import os

def is_stdlib_file(typeshed_dir: str | None, file: str) -> bool:
    if "stdlib" not in file:
        # Fast path
        return False
    typeshed_dir = typeshed_dir if typeshed_dir is not None else TYPESHED_DIR
    stdlib_dir = os.path.join(typeshed_dir, "stdlib")
    try:
        return os.path.commonpath((stdlib_dir, os.path.abspath(file))) == stdlib_dir
    except ValueError:  # Different drives on Windows
        return False

