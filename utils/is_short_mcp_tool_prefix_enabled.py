
def is_short_mcp_tool_prefix_enabled() -> bool:
    """Return True when the short-ID tool prefix mode is enabled.

    Read at call time (not import time) so tests and runtime config changes
    take effect without reimporting the module.
    """
    raw = os.environ.get("LITELLM_USE_SHORT_MCP_TOOL_PREFIX", "")
    return raw.strip().lower() in ("1", "true", "yes", "on")

