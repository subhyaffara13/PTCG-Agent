from typing import Dict

def _strip_header_whitespace(headers: Dict[str, str]) -> Dict[str, str]:
    return {
        (key.strip() if isinstance(key, str) else key): (
            value.strip() if isinstance(value, str) else value
        )
        for key, value in headers.items()
    }

