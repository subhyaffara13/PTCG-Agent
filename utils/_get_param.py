from typing import Any

def _get_param(
    litellm_params: "LitellmParams",
    guardrail: "Guardrail",
    key: str,
    default: Any = None,
) -> Any:
    """Get a param from litellm_params, with fallback to raw guardrail litellm_params (for extra fields not on LitellmParams)."""
    value = getattr(litellm_params, key, default)
    if value is not None:
        return value
    raw = guardrail.get("litellm_params")
    if isinstance(raw, dict) and key in raw:
        return raw[key]
    return default

