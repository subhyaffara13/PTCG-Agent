from typing import Any

def _override_openai_response_model(
    *,
    response_obj: Any,
    requested_model: str,
    log_context: str,
) -> None:
    """
    Force the OpenAI-compatible `model` field in the response to match what the client requested.

    LiteLLM internally prefixes some provider/deployment model identifiers (e.g. `hosted_vllm/...`).
    That internal identifier should not be returned to clients in the OpenAI `model` field.

    Note: This is intentionally verbose. A model mismatch is a useful signal that an internal
    model identifier is being stamped/preserved somewhere in the request/response pipeline.
    We log mismatches as warnings (and then restamp to the client-requested value) so these
    paths stay observable for maintainers/operators without breaking client compatibility.

    Errors are reserved for cases where the proxy cannot read/override the response model field.

    Exceptions:
    1. If a fallback occurred (indicated by x-litellm-attempted-fallbacks header),
       we preserve the actual model that was used (the fallback model).
    2. If the request was to an Azure Model Router, we preserve the actual model
       that was used (e.g., gpt-5-nano-2025-08-07) instead of the router model.
    3. If this was a fastest_response batch completion, use the winning model's
       model group name instead of the comma-separated list the client sent.
    """
    if not requested_model:
        return

    hidden_params = getattr(response_obj, "_hidden_params", {}) or {}
    if isinstance(hidden_params, dict):
        # Check if a fallback occurred - if so, preserve the actual model used
        fallback_headers = hidden_params.get("additional_headers", {}) or {}
        attempted_fallbacks = fallback_headers.get(
            "x-litellm-attempted-fallbacks", None
        )
        if attempted_fallbacks is not None and attempted_fallbacks > 0:
            verbose_proxy_logger.debug(
                "%s: fallback detected (attempted_fallbacks=%d), preserving actual model used instead of overriding to requested model.",
                log_context,
                attempted_fallbacks,
            )
            return

        # For fastest_response batch completions, use the winning model's group
        # name rather than the comma-separated list the client sent.
        if hidden_params.get("fastest_response_batch_completion"):
            winning_model = fallback_headers.get("x-litellm-model-group")
            if winning_model:
                verbose_proxy_logger.debug(
                    "%s: fastest_response detected, using winning model group=%r instead of requested=%r.",
                    log_context,
                    winning_model,
                    requested_model,
                )
                requested_model = winning_model
            else:
                verbose_proxy_logger.debug(
                    "%s: fastest_response detected but no model group header found, preserving actual model from response.",
                    log_context,
                )
                return

    # Check if this is an Azure Model Router request - if so, preserve the actual model used
    if _is_azure_model_router_request(requested_model):
        verbose_proxy_logger.debug(
            "%s: Azure Model Router detected - preserving actual model used from response instead of overriding to router model.",
            log_context,
        )
        return

    if isinstance(response_obj, dict):
        downstream_model = response_obj.get("model")
        if downstream_model != requested_model:
            verbose_proxy_logger.debug(
                "%s: response model mismatch - requested=%r downstream=%r. Overriding response['model'] to requested model.",
                log_context,
                requested_model,
                downstream_model,
            )
        response_obj["model"] = requested_model
        return

    if not hasattr(response_obj, "model"):
        verbose_proxy_logger.error(
            "%s: cannot override response model; missing `model` attribute. response_type=%s",
            log_context,
            type(response_obj),
        )
        return

    downstream_model = getattr(response_obj, "model", None)
    if downstream_model != requested_model:
        verbose_proxy_logger.debug(
            "%s: response model mismatch - requested=%r downstream=%r. Overriding response.model to requested model.",
            log_context,
            requested_model,
            downstream_model,
        )

    try:
        setattr(response_obj, "model", requested_model)
    except Exception as e:
        verbose_proxy_logger.error(
            "%s: failed to override response.model=%r on response_type=%s. error=%s",
            log_context,
            requested_model,
            type(response_obj),
            str(e),
            exc_info=True,
        )

