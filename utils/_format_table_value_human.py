import json
import re
from typing import Any

def _format_table_value_human(value: Any) -> str:
    """Convert a value to string for terminal display."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "✔" if value else ""
    if isinstance(value, datetime.datetime):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, str) and re.match(r"^\d{4}-\d{2}-\d{2}T", value):
        return value[:10]
    if isinstance(value, str):
        return _single_line(value)
    if isinstance(value, list):
        return ", ".join(_format_table_value_human(v) for v in value)
    elif isinstance(value, dict):
        if "name" in value:  # Likely to be a user or org => print name
            return _single_line(str(value["name"]))
        return _single_line(json.dumps(value))
    return _single_line(str(value))

