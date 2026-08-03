import json
from typing import Any

def _encode_json_for_header(data: Any) -> str:
    """
    JSON-serialize and URL-encode data for safe header transmission.
    """
    json_payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return quote(json_payload, safe="")

