
def _content_filter(category: str):
    """Instantiate ContentFilterGuardrail with a given category."""
    from litellm.proxy.guardrails.guardrail_hooks.litellm_content_filter.content_filter import (
        ContentFilterGuardrail,
    )

    guardrail = ContentFilterGuardrail(
        guardrail_name=f"{category}_eval",
        categories=[
            {  # type: ignore[list-item]
                "category": category,
                "enabled": True,
                "action": "BLOCK",
            }
        ],
    )
    return _ContentFilterChecker(guardrail)

