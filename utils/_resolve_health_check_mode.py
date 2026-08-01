
def _resolve_health_check_mode(
    model_info: Mapping[str, object], litellm_params: Mapping[str, object]
) -> str | None:
    """
    Effective mode for a deployment's health-check probe.

    Prefers operator-set `model_info.mode`; otherwise resolves it from the model
    cost map, which understands `bedrock/` and cross-region inference-profile
    prefixes (`us.`, `eu.`, `apac.`). Without this, non-chat Bedrock deployments
    (e.g. embeddings) are probed as chat, so `max_tokens` is injected and the
    request 400s on "extraneous key [max_tokens]".
    """
    explicit_mode = model_info.get("mode")
    if isinstance(explicit_mode, str):
        return explicit_mode
    model = litellm_params.get("model")
    if not isinstance(model, str):
        return None
    try:
        return litellm.get_model_info(model=model).get("mode")
    except Exception:
        return None

