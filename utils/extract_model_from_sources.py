
def extract_model_from_sources(
    file_id: str,
    request,  # FastAPI Request object
    data: Optional[dict] = None,
) -> tuple[Optional[str], Optional[str]]:
    """
    Extract model information from multiple sources in priority order:
    1. Embedded in file_id (highest priority)
    2. Request headers (x-litellm-model)
    3. Query parameters (?model=)
    4. Request body/data dict

    Args:
        file_id: File ID that may contain embedded model info
        request: FastAPI request object
        data: Optional request data dictionary

    Returns:
        Tuple of (model_from_id, model_from_param)
        - model_from_id: Model decoded from file ID (if embedded)
        - model_from_param: Model from header/query/body
    """
    if data is None:
        data = {}

    # Check if file_id has embedded model info
    model_from_id = decode_model_from_file_id(file_id)

    # Check other sources for model parameter
    model_from_param = (
        data.get("model")
        or request.query_params.get("model")
        or request.headers.get("x-litellm-model")
    )

    return model_from_id, model_from_param

