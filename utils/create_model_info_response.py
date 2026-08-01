
def create_model_info_response(
    model_id: str,
    provider: str,
    include_metadata: bool = False,
    fallback_type: Optional[str] = None,
    llm_router: Optional["Router"] = None,
) -> ModelInfoResponse:
    """
    Create a standardized OpenAI-compatible model object.

    When include_metadata is true, attaches the model's configured fallbacks
    (resolved via the router under fallback_type, defaulting to "general").
    Raises HTTPException(400) for an unknown fallback_type.
    """
    from litellm.proxy.auth.model_checks import get_all_fallbacks

    base: ModelInfoResponse = {
        "id": model_id,
        "object": "model",
        "created": DEFAULT_MODEL_CREATED_AT_TIME,
        "owned_by": provider,
    }

    # Surface context-window limits for OpenAI-compatible discovery clients.
    # Only emitted when known, so wildcard routes and limitless backends stay clean.
    # Limits are best-effort enrichment, so a single malformed deployment degrades
    # to the base response rather than 500-ing the whole listing.
    if llm_router is not None:
        try:
            model_group_info = llm_router.get_model_group_info(model_id)
        except Exception as e:
            verbose_proxy_logger.debug(
                "create_model_info_response: get_model_group_info failed for %s: %s",
                model_id,
                e,
            )
            model_group_info = None
        if model_group_info is not None:
            if model_group_info.max_input_tokens is not None:
                base["max_input_tokens"] = int(model_group_info.max_input_tokens)
            if model_group_info.max_output_tokens is not None:
                base["max_output_tokens"] = int(model_group_info.max_output_tokens)

    if not include_metadata:
        return base

    effective_fallback_type = fallback_type if fallback_type is not None else "general"

    valid_fallback_types = ["general", "context_window", "content_policy"]
    if effective_fallback_type not in valid_fallback_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid fallback_type. Must be one of: {valid_fallback_types}",
        )

    fallbacks = get_all_fallbacks(
        model=model_id,
        llm_router=llm_router,
        fallback_type=effective_fallback_type,
    )
    return {**base, "metadata": {"fallbacks": fallbacks}}

