from typing import Any, List

def _extract_group_values(value: Any) -> List[str]:
    """Return group ids from a SCIM patch value."""
    group_values: List[str] = []
    if isinstance(value, list):
        for v in value:
            if isinstance(v, dict) and v.get("value"):
                group_values.append(str(v.get("value")))
            elif isinstance(v, str):
                group_values.append(v)
    elif isinstance(value, dict):
        if value.get("value"):
            group_values.append(str(value.get("value")))
    elif isinstance(value, str):
        group_values.append(value)
    return group_values

