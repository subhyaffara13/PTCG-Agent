
def sanitize_mcp_alias_for_header(alias: str) -> str:
    """
    Sanitize an MCP server alias for x-mcp-{alias}-{header} HTTP headers.

    Must stay in sync with ui/litellm-dashboard/src/utils/mcpHeaderUtils.ts.
    """
    sanitized = _MCP_ALIAS_HEADER_INVALID_RE.sub("_", alias.lower().strip())
    sanitized = re.sub(r"_+", "_", sanitized)
    return sanitized.strip("_")

