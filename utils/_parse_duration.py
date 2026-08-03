import re
from typing import Optional, Tuple

def _parse_duration(duration: str) -> Tuple[Optional[int], Optional[str]]:
    """Parse the duration string into value and unit."""
    match = re.match(r"(\d+)([a-z]+)", duration)
    if not match:
        return None, None

    value, unit = match.groups()
    return int(value), unit

