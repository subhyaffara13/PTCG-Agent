from typing import Any

def effective_skip_tool_message_for_guardrail(guardrail_to_apply: Any) -> bool:
    per = getattr(guardrail_to_apply, "skip_tool_message_in_guardrail", None)
    if per is not None:
        return bool(per)
    import litellm

    return bool(getattr(litellm, "skip_tool_message_in_guardrail", False))

