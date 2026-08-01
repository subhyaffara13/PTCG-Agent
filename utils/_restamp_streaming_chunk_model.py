
def _restamp_streaming_chunk_model(
    *,
    chunk: Any,
    requested_model_from_client: str,
    request_data: dict,
    model_mismatch_logged: bool,
) -> Tuple[Any, bool]:
    # Always return the client-requested model name (not provider-prefixed internal identifiers)
    # on streaming chunks.
    #
    # Note: This warning is intentionally verbose. A mismatch is a useful signal that an
    # internal provider/deployment identifier is leaking into the public API, and helps
    # maintainers/operators catch regressions while preserving OpenAI-compatible output.
    if not requested_model_from_client or not isinstance(chunk, (BaseModel, dict)):
        return chunk, model_mismatch_logged

    # For Azure Model Router, preserve the actual model used in each chunk
    if _is_azure_model_router_request(requested_model_from_client):
        return chunk, model_mismatch_logged

    # For fastest_response batch completions, preserve the winning model's name
    # instead of stamping the comma-separated list the client sent.
    if request_data.get("fastest_response", False):
        return chunk, model_mismatch_logged

    downstream_model = (
        chunk.get("model") if isinstance(chunk, dict) else getattr(chunk, "model", None)
    )
    if downstream_model == requested_model_from_client:
        return chunk, model_mismatch_logged

    if not model_mismatch_logged and downstream_model != requested_model_from_client:
        verbose_proxy_logger.debug(
            "litellm_call_id=%s: streaming chunk model mismatch - requested=%r downstream=%r. Overriding model to requested.",
            request_data.get("litellm_call_id"),
            requested_model_from_client,
            downstream_model,
        )
        model_mismatch_logged = True

    if isinstance(chunk, dict):
        chunk["model"] = requested_model_from_client
        return chunk, model_mismatch_logged

    try:
        setattr(chunk, "model", requested_model_from_client)
    except Exception as e:
        verbose_proxy_logger.error(
            "litellm_call_id=%s: failed to override chunk.model=%r on chunk_type=%s. error=%s",
            request_data.get("litellm_call_id"),
            requested_model_from_client,
            type(chunk),
            str(e),
            exc_info=True,
        )

    return chunk, model_mismatch_logged

