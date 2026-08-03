from typing import Dict

def _merge_openapi_tool_request_headers(
    static_headers: Dict[str, str],
) -> Dict[str, str]:
    """Merge static closure headers with per-request ContextVar overrides.

    Precedence (highest to lowest):
        1. ``_request_auth_header`` — BYOK override of ``Authorization``
        2. ``static_headers`` — operator-configured headers baked into the
           tool closure at registration time
        3. ``_request_extra_headers`` — per-request headers forwarded from
           the MCP caller (allowlisted by ``MCPServer.extra_headers``)

    This matches the existing MCP invariant in
    :func:`litellm.proxy._experimental.mcp_server.utils.merge_mcp_headers`
    and the managed MCP path, where ``static_headers`` always wins over
    caller-forwarded headers. Keeping the same precedence here prevents an
    authenticated caller from overriding an operator-configured value
    (e.g. a tenant id or upstream API key) by sending the same header name.

    Header names are compared case-insensitively so different casing cannot
    bypass the precedence rules.
    """
    request_extra = _request_extra_headers.get() or {}
    static = static_headers or {}

    static_lower_names = {k.lower() for k in static}
    effective_headers: Dict[str, str] = {
        k: v for k, v in request_extra.items() if k.lower() not in static_lower_names
    }
    effective_headers.update(static)

    override_auth = _request_auth_header.get()
    if override_auth:
        for existing in [k for k in effective_headers if k.lower() == "authorization"]:
            del effective_headers[existing]
        effective_headers["Authorization"] = override_auth

    return effective_headers

