
def get_policies_summary() -> Dict[str, Any]:
    """
    Get a summary of loaded policies for debugging/display.

    Returns:
        Dictionary with policy information
    """
    from litellm.proxy.policy_engine.policy_resolver import PolicyResolver

    policy_registry = get_policy_registry()
    attachment_registry = get_attachment_registry()

    if not policy_registry.is_initialized():
        return {"initialized": False, "policies": {}, "attachments": []}

    resolved = PolicyResolver.get_all_resolved_policies()

    summary: Dict[str, Any] = {
        "initialized": True,
        "policy_count": len(resolved),
        "attachment_count": len(attachment_registry.get_all_attachments()),
        "policies": {},
        "attachments": [],
    }

    for policy_name, resolved_policy in resolved.items():
        policy = policy_registry.get_policy(policy_name)
        summary["policies"][policy_name] = {
            "inherit": policy.inherit if policy else None,
            "description": policy.description if policy else None,
            "guardrails_add": policy.guardrails.get_add() if policy else [],
            "guardrails_remove": policy.guardrails.get_remove() if policy else [],
            "condition": (
                policy.condition.model_dump() if policy and policy.condition else None
            ),
            "resolved_guardrails": resolved_policy.guardrails,
            "inheritance_chain": resolved_policy.inheritance_chain,
        }

    # Add attachment info
    for attachment in attachment_registry.get_all_attachments():
        summary["attachments"].append(
            {
                "policy": attachment.policy,
                "scope": attachment.scope,
                "teams": attachment.teams,
                "keys": attachment.keys,
                "models": attachment.models,
            }
        )

    return summary

