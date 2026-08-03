import re

def _modeling_key(file_path: str) -> str | None:
    # Extract "xxx" from test_modeling_xxx.py
    m = re.search(r"test_modeling_([A-Za-z0-9_]+)\.py$", file_path)
    if m:
        return m.group(1)
    return None

