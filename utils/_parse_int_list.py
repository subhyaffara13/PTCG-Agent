from typing import Any

def _parse_int_list(value: Any) -> list[int] | None:
    if isinstance(value, list):
        try:
            return [int(x) for x in value]
        except (TypeError, ValueError):
            return None
    if isinstance(value, str):
        match = _INT_LIST_RE.search(value)
        if match:
            try:
                return [int(x.strip()) for x in match.group(1).split(",")]
            except ValueError:
                return None
    return None

