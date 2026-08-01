
def _get_embedding_url(
    model: str,
    vertex_project: Optional[str],
    vertex_location: Optional[str],
    vertex_api_version: Literal["v1", "v1beta1"],
) -> Tuple[str, str]:
    """
    Get URL for embedding models.

    Handles special patterns:
    - bge/endpoint_id -> strips to endpoint_id for endpoints/ routing
    - numeric model -> routes to endpoints/
    - regular model -> routes to publishers/google/models/
    - models with uses_embed_content flag -> use embedContent endpoint instead of predict
    """
    original_model = model
    model = get_vertex_base_model_name(model=model)

    try:
        model_info = litellm.get_model_info(
            model=original_model,
            custom_llm_provider="vertex_ai",
        )
        uses_embed_content = model_info.get("uses_embed_content", False)
    except Exception:
        uses_embed_content = False

    endpoint = "embedContent" if uses_embed_content else "predict"

    base_url = get_vertex_base_url(vertex_location)

    if model.isdigit():
        url = f"{base_url}/{vertex_api_version}/projects/{vertex_project}/locations/{vertex_location}/endpoints/{model}:{endpoint}"
    else:
        url = f"{base_url}/v1/projects/{vertex_project}/locations/{vertex_location}/publishers/google/models/{model}:{endpoint}"

    return url, endpoint

