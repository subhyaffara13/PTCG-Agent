from typing import Optional, Tuple

def _resolve_provider_from_router_alias(
    model: str,
) -> Optional[Tuple[str, str]]:
    """
    Resolve a router ``model_name`` alias to ``(underlying_model, provider)``
    by scanning the active router's ``model_list``.

    Returns ``None`` if the router isn't initialized, the alias isn't
    registered, the deployment has no usable ``litellm_params.model``, or
    any underlying lookup raises. Callers fall through to the defensive
    ``litellm_proxy`` fallback in that case — never raising secondary
    exceptions out of the rate-limit raise path.
    """
    try:
        from litellm.proxy.proxy_server import llm_router
    except Exception:
        return None
    if llm_router is None:
        return None
    try:
        model_list = getattr(llm_router, "model_list", None)
        if not model_list:
            return None
        for deployment in model_list:
            if not isinstance(deployment, dict):
                continue
            if deployment.get("model_name") != model:
                continue
            params = deployment.get("litellm_params")
            if not isinstance(params, dict):
                continue
            underlying_model = params.get("model")
            if not isinstance(underlying_model, str) or not underlying_model:
                continue
            try:
                resolved_model, custom_llm_provider, _, _ = litellm.get_llm_provider(
                    model=underlying_model,
                )
            except Exception:
                continue
            if not custom_llm_provider:
                continue
            # Prefer the underlying provider-qualified model so the failure
            # callback / Prometheus label points at the actual deployment, not
            # the alias.
            return (
                resolved_model or underlying_model,
                custom_llm_provider,
            )
        return None
    except Exception:
        return None

