from typing import Any, Dict, Optional

def _get_user_api_key_auth_from_kwargs(kwargs: Dict[str, Any]) -> Optional[Any]:
    for metadata_key in ("metadata", "litellm_metadata"):
        metadata = kwargs.get(metadata_key)
        if isinstance(metadata, dict) and metadata.get("user_api_key_auth") is not None:
            return metadata["user_api_key_auth"]
    return None

