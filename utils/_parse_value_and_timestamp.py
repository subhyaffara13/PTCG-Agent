from typing import Optional, Tuple

def _parse_value_and_timestamp(s: str) -> Tuple[float, Optional[float]]:
    s = s.lstrip()
    separator = " "
    if separator not in s:
        separator = "\t"
    values = [value.strip() for value in s.split(separator) if value.strip()]
    if not values:
        return float(s), None
    value = _parse_value(values[0])
    timestamp = (_parse_value(values[-1]) / 1000) if len(values) > 1 else None
    return value, timestamp

