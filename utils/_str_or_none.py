from typing import Optional

def _str_or_none(value) -> Optional[str]:
    try:
        return str(value) if value is not None else None
    except Exception:
        return None

