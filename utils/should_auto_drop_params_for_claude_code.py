
def should_auto_drop_params_for_claude_code(
    user_agent: str, data: dict, proxy_config: ProxyConfig
) -> bool:
    """drop_params defaults to on for Claude Code so its Anthropic-specific
    params (e.g. thinking) don't fail requests routed to non-Anthropic
    providers. An explicit drop_params from the caller or in the operator's
    ``litellm_settings`` always wins over this default."""
    if not is_claude_code_user_agent(user_agent):
        return False
    if "drop_params" in data:
        return False
    config = getattr(proxy_config, "config", None)
    litellm_settings = (
        config.get("litellm_settings") if isinstance(config, dict) else None
    )
    return not (
        isinstance(litellm_settings, dict) and "drop_params" in litellm_settings
    )

