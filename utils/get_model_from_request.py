
def get_model_from_request(
    request_data: dict,
    route: str,
    request_headers: Optional[Mapping[str, Any]] = None,
    request_query_params: Optional[Mapping[str, Any]] = None,
    llm_router: Optional[Router] = None,
) -> Optional[Union[str, List[str]]]:
    candidates = _extract_model_candidates_from_request(
        request_data=request_data,
        route=route,
        request_headers=request_headers,
        request_query_params=request_query_params,
        llm_router=llm_router,
    )
    model = _format_model_candidates(candidates)

    # If no explicit model was found, try to extract from route
    if model is None:
        # Parse model from route that follows the pattern /openai/deployments/{model}/*
        match = re.match(r"/openai/deployments/([^/]+)", route)
        if match:
            model = match.group(1)

    # If still not found, extract model from Google generateContent-style routes.
    # These routes put the model in the path and allow "/" inside the model id.
    # Examples:
    # - /v1beta/models/gemini-2.0-flash:generateContent
    # - /v1beta/models/bedrock/claude-sonnet-3.7:generateContent
    # - /models/custom/ns/model:streamGenerateContent
    if model is None and not route.lower().startswith("/vertex"):
        google_match = re.search(r"/(?:v1beta|beta)/models/([^:]+):", route)
        if google_match:
            model = google_match.group(1)

    if model is None and not route.lower().startswith("/vertex"):
        google_match = re.search(r"^/models/([^:]+):", route)
        if google_match:
            model = google_match.group(1)

    # If still not found, extract from Vertex AI passthrough route
    # Pattern: /vertex_ai/.../models/{model_id}:*
    # Example: /vertex_ai/v1/.../models/gemini-1.5-pro:generateContent
    if model is None and route.lower().startswith("/vertex"):
        vertex_match = re.search(r"/models/([^:]+)", route)
        if vertex_match:
            model = vertex_match.group(1)

    return model

