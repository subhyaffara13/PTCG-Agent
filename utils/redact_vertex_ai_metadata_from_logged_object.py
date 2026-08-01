
def redact_vertex_ai_metadata_from_logged_object(obj: Any) -> None:
    if isinstance(obj, dict):
        for field in VERTEX_AI_PROVIDER_METADATA_FIELDS:
            if field in obj:
                obj[field] = []
        hidden_params = obj.get("_hidden_params")
        if isinstance(hidden_params, dict):
            for field in VERTEX_AI_PROVIDER_METADATA_FIELDS:
                hidden_params.pop(field, None)
        return

    for field in VERTEX_AI_PROVIDER_METADATA_FIELDS:
        if hasattr(obj, field):
            setattr(obj, field, [])
    hidden_params = getattr(obj, "_hidden_params", None)
    if isinstance(hidden_params, dict):
        for field in VERTEX_AI_PROVIDER_METADATA_FIELDS:
            hidden_params.pop(field, None)

