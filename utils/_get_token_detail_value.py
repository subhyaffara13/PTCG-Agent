from typing import Optional

def _get_token_detail_value(details: object, key: str) -> Optional[int]:
    if isinstance(details, dict):
        value = details.get(key)
    else:
        value = getattr(details, key, None)
    return value if isinstance(value, int) else None

