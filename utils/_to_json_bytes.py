import json
from typing import Any

def _to_json_bytes(obj: Any) -> bytes:
    return json.dumps(_dataclass_to_dict(obj), cls=EnumEncoder, allow_nan=False).encode(
        "utf-8"
    )

