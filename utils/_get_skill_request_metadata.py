from typing import Any, Dict, Optional

def _get_skill_request_metadata(
    kwargs: Dict[str, Any],
    extra_body: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    if extra_body and isinstance(extra_body.get("metadata"), dict):
        return extra_body["metadata"]

    metadata = kwargs.get("metadata")
    if isinstance(metadata, dict) and isinstance(
        metadata.get("requester_metadata"), dict
    ):
        return metadata["requester_metadata"]
    return None

