from typing import Optional, Tuple

def _get_vertex_url(
    mode: all_gemini_url_modes,
    model: str,
    stream: Optional[bool],
    vertex_project: Optional[str],
    vertex_location: Optional[str],
    vertex_api_version: Literal["v1", "v1beta1"],
) -> Tuple[str, str]:
    url: Optional[str] = None
    endpoint: Optional[str] = None

    model = litellm.VertexGeminiConfig.get_model_for_vertex_ai_url(model=model)

    if mode == "chat":
        ### SET RUNTIME ENDPOINT ###
        endpoint = "generateContent"
        base_url = get_vertex_base_url(vertex_location)

        if stream is True:
            endpoint = "streamGenerateContent"

        # if model is only numeric chars then it's a fine tuned gemini model
        # model = 4965075652664360960
        # send to this url: url = f"{base_url}/{version}/projects/{vertex_project}/locations/{vertex_location}/endpoints/{model}:{endpoint}"
        if model.isdigit():
            # It's a fine-tuned Gemini model - use endpoints/ path
            url = f"{base_url}/{vertex_api_version}/projects/{vertex_project}/locations/{vertex_location}/endpoints/{model}:{endpoint}"
        else:
            # Regular model - use publishers/google/models/ path
            url = f"{base_url}/{vertex_api_version}/projects/{vertex_project}/locations/{vertex_location}/publishers/google/models/{model}:{endpoint}"

        if stream is True:
            url += "?alt=sse"
    elif mode == "embedding":
        return _get_embedding_url(
            model=model,
            vertex_project=vertex_project,
            vertex_location=vertex_location,
            vertex_api_version=vertex_api_version,
        )
    elif mode == "image_generation":
        endpoint = "predict"
        base_url = get_vertex_base_url(vertex_location)
        if model.isdigit():
            # Numeric model -> custom endpoint
            url = f"{base_url}/{vertex_api_version}/projects/{vertex_project}/locations/{vertex_location}/endpoints/{model}:{endpoint}"
        else:
            # Regular model -> publisher model
            url = f"{base_url}/v1/projects/{vertex_project}/locations/{vertex_location}/publishers/google/models/{model}:{endpoint}"
    elif mode == "count_tokens":
        endpoint = "countTokens"
        base_url = get_vertex_base_url(vertex_location)
        url = f"{base_url}/{vertex_api_version}/projects/{vertex_project}/locations/{vertex_location}/publishers/google/models/{model}:{endpoint}"
    if not url or not endpoint:
        raise ValueError(f"Unable to get vertex url/endpoint for mode: {mode}")
    return url, endpoint

