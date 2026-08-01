
def pop_vertex_request_labels(
    optional_params: Optional[dict],
    litellm_params: Optional[dict],
) -> Optional[Dict[str, str]]:
    """
    Resolve labels from optional ``labels`` (Gemini-style) and/or
    ``litellm_params["metadata"]`` / ``litellm_params["litellm_metadata"]``
    (``requester_metadata``). Pops ``labels`` from optional_params when present.
    """
    labels: Optional[Dict[str, str]] = None
    if optional_params is not None and "labels" in optional_params:
        raw = optional_params.pop("labels")
        if isinstance(raw, dict):
            labels = {k: v for k, v in raw.items() if isinstance(v, str)}
    if not labels:
        labels = vertex_request_labels_from_litellm_params(litellm_params)
    return labels if labels else None

