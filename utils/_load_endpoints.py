import json
from typing import Any, Dict, List

def _load_endpoints() -> List[Dict[str, Any]]:
    raw = json.loads(
        files("litellm")
        .joinpath("provider_endpoints_support_backup.json")
        .read_text(encoding="utf-8")
    )
    return _build_endpoints(raw)

