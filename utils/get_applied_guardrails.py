from typing import Any, Dict, List

def get_applied_guardrails(kwargs: Dict[str, Any]) -> List[str]:
    """
    - Add 'default_on' guardrails to the list
    - Add request guardrails to the list
    """

    request_guardrails = get_request_guardrails(kwargs)
    applied_guardrails = []
    CustomGuardrail = _get_cached_custom_guardrail()
    for callback in litellm.callbacks:
        if callback is not None and isinstance(callback, CustomGuardrail):
            if callback.guardrail_name is not None:
                if callback.default_on is True:
                    applied_guardrails.append(callback.guardrail_name)
                elif callback.guardrail_name in request_guardrails:
                    applied_guardrails.append(callback.guardrail_name)

    return applied_guardrails

