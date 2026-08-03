from typing import Any, Dict, Optional

def should_use_xai_oauth(litellm_params: Optional[Dict[str, Any]]) -> bool:
    return bool((litellm_params or {}).get("use_xai_oauth"))

