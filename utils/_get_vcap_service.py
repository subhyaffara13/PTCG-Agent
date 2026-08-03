from typing import Any, Dict, Optional

def _get_vcap_service(label: str) -> Optional[Dict[str, Any]]:
    for services in _load_vcap().values():
        for svc in services:
            if svc.get("label") == label:
                return svc
    return None

