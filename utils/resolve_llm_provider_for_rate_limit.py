from typing import Optional, Tuple

def resolve_llm_provider_for_rate_limit(
    model: Optional[str],
) -> Tuple[str, str]:
    """
    Resolve ``(model, llm_provider)`` for a request being rejected by an
    internal proxy-side rate-limit hook.

    These hooks fire from ``async_pre_call_hook`` — well before
    :func:`litellm.get_llm_provider` is invoked anywhere else in the request
    lifecycle — so the raised 429 would otherwise have an empty
    ``llm_provider`` field, making the resulting Prometheus
    ``litellm_proxy_failed_requests_metric`` show up with
    ``exception_class="RateLimitError"`` and no provider attribution.

    Resolution order:

    1. ``litellm.get_llm_provider(model)`` — covers raw provider/model
       strings the SDK already understands (``"gpt-4o-mini"``,
       ``"anthropic/claude-3-5-sonnet"``, ``"bedrock/..."`` etc.).
    2. **Router alias fallback** — nearly every real proxy deployment
       routes through a router ``model_name`` alias (e.g.
       ``"tpm-locked"`` → ``litellm_params.model: openai/gpt-4o-mini``).
       ``get_llm_provider`` doesn't know router aliases, so without this
       step every alias call ended up labeled ``"litellm_proxy"``,
       defeating the field's purpose for the most common case.
    3. Defensive fallback to ``("", "litellm_proxy")`` — used only when
       ``model`` is missing, malformed, or both lookups fail. We never let
       a secondary exception escape and mask the rate-limit error we're
       trying to surface.
    """
    if not model:
        return "", PROXY_LLM_PROVIDER_FALLBACK
    try:
        resolved_model, custom_llm_provider, _, _ = litellm.get_llm_provider(
            model=model,
        )
        return (
            resolved_model or model,
            custom_llm_provider or PROXY_LLM_PROVIDER_FALLBACK,
        )
    except Exception as e:
        alias_resolution = _resolve_provider_from_router_alias(model)
        if alias_resolution is not None:
            return alias_resolution
        verbose_proxy_logger.debug(
            "rate_limiter_utils.resolve_llm_provider_for_rate_limit: "
            "could not resolve provider for model=%s, falling back to %s. err=%s",
            model,
            PROXY_LLM_PROVIDER_FALLBACK,
            str(e),
        )
        return model, PROXY_LLM_PROVIDER_FALLBACK

