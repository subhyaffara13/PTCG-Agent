from typing import Any, Dict

def _extract_field_type(field_info: Dict[str, Any]) -> str:
    """Extract the non-null type from a Pydantic v2 JSON schema field."""
    if "type" in field_info:
        return field_info["type"]
    for option in field_info.get("anyOf", []):
        if option.get("type") != "null":
            return option.get("type", "string")
    return "string"

