from typing import Any, Optional

def _merge_metadata_bags(request_data: Mapping[str, Any]) -> Optional[dict[str, Any]]:
    merged: dict[str, Any] = {}
    present = False
    for bag in (request_data.get("metadata"), request_data.get("litellm_metadata")):
        if isinstance(bag, Mapping):
            present = True
            merged.update(bag)
    return merged if present else None

