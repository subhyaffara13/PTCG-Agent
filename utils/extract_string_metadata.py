from typing import Any

def extract_string_metadata(input: str) -> dict[str, Any]:
    assert isinstance(input, str)
    metadata: dict[str, Any] = {}
    metadata["string_value"] = input
    return metadata

