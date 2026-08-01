
def _get_litellm_param(
    litellm_params: "LitellmParams",
    guardrail: "Guardrail",
    key: str,
    default: Any = None,
) -> Any:
    val = getattr(litellm_params, key, None)
    if val is not None:
        return val
    raw = guardrail.get("litellm_params")
    if isinstance(raw, dict) and key in raw:
        return raw[key]
    if raw is not None and not isinstance(raw, dict):
        attr = getattr(raw, key, None)
        if attr is not None:
            return attr
    return default

