from typing import Any, Optional

def _get_case_insensitive_mapping_value(
    mapping: Optional[Mapping[str, Any]], key: str
) -> Any:
    if not mapping:
        return None
    if key in mapping:
        return mapping[key]
    key_lower = key.lower()
    for mapping_key, value in mapping.items():
        if str(mapping_key).lower() == key_lower:
            return value
    return None

