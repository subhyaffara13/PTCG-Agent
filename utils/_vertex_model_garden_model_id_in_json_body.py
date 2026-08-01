
def _vertex_model_garden_model_id_in_json_body(model: str) -> bool:
    """
    Vertex catalog / publisher models are addressed as publisher/model (e.g.
    xai/grok-4.1-fast-reasoning) on the shared OpenAPI URL, with the id in the JSON body.

    Deployed Model Garden endpoints are typically a single segment (often numeric)
    and use .../endpoints/{ENDPOINT_ID}/chat/completions with an empty model field.
    """
    return "/" in model

