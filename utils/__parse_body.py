import json
from typing import Any

def __parse_body(body) -> Any:
    try:
        return json.loads(body)
    except Exception as e:
        return {}

