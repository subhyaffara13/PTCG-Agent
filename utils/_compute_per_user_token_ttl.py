
def _compute_per_user_token_ttl(server: "MCPServer", expires_in: Optional[int]) -> int:
    """Compute Redis TTL for a per-user token.

    Uses server.token_storage_ttl_seconds when configured; otherwise derives
    TTL from expires_in minus the expiry buffer; falls back to the default TTL.
    """
    if server.token_storage_ttl_seconds is not None:
        return max(server.token_storage_ttl_seconds, 1)
    if expires_in is not None:
        return max(
            expires_in - MCP_PER_USER_TOKEN_EXPIRY_BUFFER_SECONDS,
            1,
        )
    return MCP_PER_USER_TOKEN_DEFAULT_TTL

