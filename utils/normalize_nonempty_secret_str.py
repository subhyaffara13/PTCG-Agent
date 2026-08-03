from typing import Optional

def normalize_nonempty_secret_str(val: Optional[str]) -> Optional[str]:
    """
    Strip whitespace and treat None, '', and whitespace-only strings as unset.

    Use when pairing secrets (mutual exclusion, optional auth) so whitespace-only
    values do not count as present.
    """
    if val is None:
        return None
    stripped = val.strip()
    return stripped if stripped else None

