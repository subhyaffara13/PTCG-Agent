
def _resolve_guardrail_input_type(
    active_guardrail: CustomGuardrail, input_type: str
) -> Literal["request", "response"]:
    """Return the effective input_type, auto-upgrading to 'response' for post_call guardrails."""
    if input_type == "request":
        hook = getattr(active_guardrail, "event_hook", None)
        if hook == GuardrailEventHooks.post_call or hook == "post_call":
            return "response"
    return "response" if input_type == "response" else "request"

