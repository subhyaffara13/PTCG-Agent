from typing import Any

def process_skipna(skipna: bool | ndarray | None, args) -> tuple[bool, Any]:
    if isinstance(skipna, ndarray) or skipna is None:
        args = (skipna, *args)
        skipna = True

    return skipna, args

