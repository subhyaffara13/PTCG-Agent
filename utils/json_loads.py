import json
from typing import Any

def json_loads(data: bytes) -> Any:
    if orjson is not None:
        return orjson.loads(data)
    return json.loads(data)

