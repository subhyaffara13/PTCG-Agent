
def _google_genai_streaming_hidden_params(
    *,
    api_base: str,
    litellm_params: GenericLiteLLMParams,
    logging_obj: LiteLLMLoggingObj,
    response_headers: httpx.Headers,
) -> Dict[str, Any]:
    """Pre-stream metadata for proxy response headers (mirrors CustomStreamWrapper._hidden_params)."""
    from litellm.litellm_core_utils.core_helpers import process_response_headers

    _model_info: Dict[str, Any] = dict(
        getattr(litellm_params, "model_info", None) or {}
    )
    _raw_id = _model_info.get("id") or logging_obj.get_router_model_id() or ""
    _model_id = _raw_id if isinstance(_raw_id, str) else str(_raw_id)
    return {
        "model_id": _model_id,
        "api_base": api_base,
        "cache_key": "",
        "response_cost": "",
        "additional_headers": process_response_headers(response_headers),
    }

