
def extract_and_build_metadata(
    opik_metadata: Dict[str, Any],
    standard_logging_metadata: Dict[str, Any],
    standard_logging_object: Dict[str, Any],
    litellm_kwargs: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build the complete metadata dictionary from all available sources.

    This combines:
    - Opik-specific metadata (tags, etc.)
    - Standard logging metadata
    - Fields from standard_logging_object (model info, status, etc.)
    - Cost information from litellm_kwargs (calculated after completion)

    Args:
        opik_metadata: Opik-specific metadata from request
        standard_logging_metadata: Standard logging metadata
        standard_logging_object: Full standard logging object with call details
        litellm_kwargs: Original LiteLLM kwargs (includes response_cost)

    Returns:
        Complete metadata dictionary for trace/span
    """
    # Start with opik metadata (excluding current_span_data which is used for trace linking)
    metadata = {k: v for k, v in opik_metadata.items() if k != "current_span_data"}
    metadata["created_from"] = "litellm"

    # Merge with standard logging metadata
    metadata.update(standard_logging_metadata)

    # Add fields from standard_logging_object
    # These come from the LiteLLM logging infrastructure
    field_mappings = {
        "call_type": "type",
        "status": "status",
        "model": "model",
        "model_id": "model_id",
        "model_group": "model_group",
        "api_base": "api_base",
        "cache_hit": "cache_hit",
        "saved_cache_cost": "saved_cache_cost",
        "error_str": "error_str",
        "model_parameters": "model_parameters",
        "hidden_params": "hidden_params",
        "model_map_information": "model_map_information",
    }

    for source_key, dest_key in field_mappings.items():
        if source_key in standard_logging_object:
            metadata[dest_key] = standard_logging_object[source_key]

    # Add cost information
    # response_cost is calculated by LiteLLM after completion and added to kwargs
    # See: litellm/litellm_core_utils/llm_response_utils/response_metadata.py
    if "response_cost" in litellm_kwargs:
        metadata["cost"] = {
            "total_tokens": litellm_kwargs["response_cost"],
            "currency": "USD",
        }

    # Add debug info if cost calculation failed
    if "response_cost_failure_debug_info" in litellm_kwargs:
        metadata["response_cost_failure_debug_info"] = litellm_kwargs[
            "response_cost_failure_debug_info"
        ]

    return metadata

