
def _get_cached_custom_guardrail():
    """
    Get cached CustomGuardrail class.
    Lazy imports on first call to avoid loading custom_guardrail at import time.
    Subsequent calls use cached class for better performance.
    """
    global _CustomGuardrail
    if _CustomGuardrail is None:
        from litellm.integrations.custom_guardrail import CustomGuardrail

        _CustomGuardrail = CustomGuardrail
    return _CustomGuardrail

