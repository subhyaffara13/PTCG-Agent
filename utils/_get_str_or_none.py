from typing import Any, Optional

def _get_str_or_none(value: Any) -> Optional[str]:
    """Cast config value to Optional[str]."""
    return str(value) if value is not None else None


def _get_str_or_none(value: Any) -> Optional[str]:
    """Cast config value to Optional[str]."""
    return str(value) if value is not None else None

