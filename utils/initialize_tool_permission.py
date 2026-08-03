from typing import Any, Dict, List, Optional

def initialize_tool_permission(litellm_params: LitellmParams, guardrail: Guardrail):
    from litellm.proxy.guardrails.guardrail_hooks.tool_permission import (
        ToolPermissionGuardrail,
    )

    rules: Optional[List[Dict[str, Any]]] = None
    if litellm_params.rules:
        rules = []
        for rule in litellm_params.rules:
            if hasattr(rule, "model_dump"):
                rules.append(rule.model_dump())
            else:
                rules.append(dict(rule))

    _tool_permission_callback = ToolPermissionGuardrail(
        guardrail_name=guardrail.get("guardrail_name", ""),
        event_hook=litellm_params.mode,
        rules=rules,
        default_action=getattr(litellm_params, "default_action", "deny"),
        on_disallowed_action=getattr(litellm_params, "on_disallowed_action", "block"),
        default_on=litellm_params.default_on,
        violation_message_template=litellm_params.violation_message_template,
    )
    litellm.logging_callback_manager.add_litellm_callback(_tool_permission_callback)
    return _tool_permission_callback

