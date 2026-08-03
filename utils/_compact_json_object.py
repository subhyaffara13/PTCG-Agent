import json
from typing import Any

def _compact_json_object(**kwargs: Any) -> bytes:
  return json.dumps(
      kwargs, sort_keys=True, indent=0, separators=(",", ":")
  ).encode("ascii")

