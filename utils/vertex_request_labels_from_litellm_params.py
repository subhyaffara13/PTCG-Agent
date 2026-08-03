from typing import Dict, Optional

def vertex_request_labels_from_litellm_params(
    litellm_params: Optional[dict],
) -> Optional[Dict[str, str]]:
    """
    Build Vertex/GCP billing labels from LiteLLM user metadata on ``litellm_params``:
    ``metadata`` (``completion(..., metadata=...)``) or ``litellm_metadata``,
    using ``requester_metadata`` string key-value pairs (same convention as Gemini).
    ``metadata`` is tried first when both are present.
    """
    if not litellm_params:
        return None
    for key in ("metadata", "litellm_metadata"):
        if key not in litellm_params:
            continue
        metadata = litellm_params[key]
        if metadata is None or not isinstance(metadata, dict):
            continue
        if "requester_metadata" not in metadata:
            continue
        rm = metadata["requester_metadata"]
        if not isinstance(rm, dict):
            continue
        labels = {k: v for k, v in rm.items() if isinstance(v, str)}
        if labels:
            return labels
    return None

