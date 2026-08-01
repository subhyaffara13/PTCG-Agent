
def redact_vertex_ai_metadata_from_litellm_params(model_call_details: dict) -> None:
    """
    success_handler() merges response._hidden_params into
    litellm_params.metadata['hidden_params'] before redaction runs, so the Vertex
    metadata must be scrubbed from that copy too.
    """
    litellm_params = model_call_details.get("litellm_params")
    if not isinstance(litellm_params, dict):
        return

    for metadata_key in ("metadata", "litellm_metadata"):
        metadata = litellm_params.get(metadata_key)
        if not isinstance(metadata, dict):
            continue
        hidden_params = metadata.get("hidden_params")
        if not isinstance(hidden_params, dict):
            continue
        for field in VERTEX_AI_PROVIDER_METADATA_FIELDS:
            hidden_params.pop(field, None)

