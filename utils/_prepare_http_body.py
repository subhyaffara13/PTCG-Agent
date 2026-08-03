import json
from typing import Any, Dict, Optional, Tuple

def _prepare_http_body(
    body: Optional[Any],
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Prepare body arguments for HTTP request - returns (json_body, data_body)."""
    if body is None:
        return None, None
    if isinstance(body, dict):
        return body, None
    if isinstance(body, list):
        return None, json.dumps(body)
    if isinstance(body, str):
        return None, body
    return None, str(body)

