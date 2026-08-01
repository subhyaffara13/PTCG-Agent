
def get_tool_policy_registry() -> ToolPolicyRegistry:
    """Return the global ToolPolicyRegistry singleton."""
    global _tool_policy_registry
    if _tool_policy_registry is None:
        _tool_policy_registry = ToolPolicyRegistry()
    return _tool_policy_registry

