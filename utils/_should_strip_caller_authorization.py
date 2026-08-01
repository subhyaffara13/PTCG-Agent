
def _should_strip_caller_authorization(
    mcp_server: MCPServer,
    raw_headers: Optional[Dict[str, str]],
    user_api_key_auth: Optional[UserAPIKeyAuth],
) -> bool:
    """Decide whether the caller's ``Authorization`` header must NOT be
    forwarded upstream when populating ``extra_headers`` for an MCP server.

    Centralized so ``_call_regular_mcp_tool`` (this module) and
    ``_prepare_mcp_server_headers`` (``server.py``) cannot drift apart on
    this security-sensitive decision.

    Strip rules:
    - **M2M (client_credentials) servers**: never forward the caller's
      ``Authorization`` — the proxy fetches its own upstream token.
    - **OAuth pass-through servers**: strip when the ``Authorization``
      header is actually the LiteLLM API key — either because admission
      validated it (``user_api_key_auth.api_key`` is set) and the caller
      did NOT also supply ``x-litellm-api-key`` to disambiguate, or
      because the legacy ``user_api_key_auth is None`` call sites did
      not supply an explicit admission header.  In the anonymous /
      pass-through cold-start case (RFC 9728) the bearer in
      ``Authorization`` is the upstream OAuth token and must be
      forwarded, so we keep it.
    """
    if mcp_server.has_client_credentials:
        return True
    if not mcp_server.is_oauth_passthrough:
        return False

    normalized_raw_headers = {
        str(k).lower(): v for k, v in (raw_headers or {}).items() if isinstance(k, str)
    }
    has_explicit_litellm_admission_header = (
        normalized_raw_headers.get("x-litellm-api-key") is not None
    )
    admission_consumed_authorization_as_litellm_key = (
        user_api_key_auth is not None
        and bool(getattr(user_api_key_auth, "api_key", None))
        and not has_explicit_litellm_admission_header
    )
    return admission_consumed_authorization_as_litellm_key or (
        user_api_key_auth is None and not has_explicit_litellm_admission_header
    )

