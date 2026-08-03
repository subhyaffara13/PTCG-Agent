from typing import Optional

def handle_model_based_routing(
    file_id: str,
    request,  # FastAPI Request object
    llm_router,  # Router instance
    data: dict,
    check_file_id_encoding: bool = True,
) -> tuple[bool, Optional[str], Optional[str], Optional[dict]]:
    """
    Orchestrate model-based credential routing for file operations.

    Args:
        file_id: File ID (may contain embedded model info)
        request: FastAPI request object
        llm_router: LiteLLM Router instance
        data: Request data dictionary
        check_file_id_encoding: Whether to check for embedded model in file_id

    Returns:
        Tuple of (should_use_model_routing, model_used, original_file_id, credentials)
        - should_use_model_routing: True if model-based routing should be used
        - model_used: The model name being used
        - original_file_id: Decoded file ID (if it was encoded)
        - credentials: Model credentials dict

    Raises:
        HTTPException: If router unavailable or model not found
    """
    model_from_id, model_from_param = extract_model_from_sources(
        file_id=file_id,
        request=request,
        data=data,
    )

    # Priority 1: Model embedded in file_id
    if check_file_id_encoding and model_from_id is not None:
        credentials = get_credentials_for_model(
            llm_router=llm_router,
            model_id=model_from_id,
            operation_context=f"file operation (file created with model '{model_from_id}')",
        )
        original_file_id = get_original_file_id(file_id)
        return True, model_from_id, original_file_id, credentials

    # Priority 2: Model from header/query/body
    elif model_from_param is not None:
        credentials = get_credentials_for_model(
            llm_router=llm_router,
            model_id=model_from_param,
            operation_context="file operation",
        )
        return True, model_from_param, None, credentials

    # No model-based routing needed
    return False, None, None, None

