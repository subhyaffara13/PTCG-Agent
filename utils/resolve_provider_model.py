
def resolve_provider_model(payload: "StandardLoggingPayload") -> str | None:
    """The model litellm dispatched to the provider, from the payload.

    Prefers the explicit ``hidden_params.litellm_model_name`` (set on call paths
    that know it, e.g. files), then the top-level ``model`` — which
    ``reconstruct_model_name`` has already resolved to the deployment's
    provider-prefixed name. Returns ``None`` only when neither is present.
    """
    raw_meta = cast(Mapping[str, object], payload.get("metadata") or {})
    hidden = cast(Mapping[str, object], payload.get("hidden_params") or {})
    return (
        # ``deployment`` survives only on paths that don't strip it from metadata;
        # harmless (and most precise) to prefer it when present.
        as_str(raw_meta.get("deployment"))
        or as_str(hidden.get("litellm_model_name"))
        or as_str(payload.get("model"))
    )

