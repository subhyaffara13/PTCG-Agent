from typing import Any, Dict

def _load_vcap() -> Dict[str, Any]:
    return _load_json_env(VCAP_SERVICES_ENV_VAR) or {}

