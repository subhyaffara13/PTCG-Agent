
def _build_sampling_request(
    raw_headers: Optional[Dict[str, str]] = None,
    client_ip: Optional[str] = None,
) -> Any:
    """Build a synthetic FastAPI Request for sampling sub-calls.

    Converts the original MCP connection's HTTP headers into ASGI
    scope format so that ``add_litellm_data_to_request`` can apply
    header-dependent guardrails, tag-based routing, trace correlation,
    and ``forward_llm_provider_auth_headers``.

    Key fields populated:
    - **headers**: All original HTTP headers are forwarded (except
      hop-by-hop: content-length, transfer-encoding).  This ensures
      ``traceparent``, ``authorization``, ``user-agent``, and
      ``x-litellm-api-key`` are visible to pre-call utils.
    - **client**: The ASGI ``(host, port)`` tuple so that
      ``request.client.host`` returns the real client IP for
      IP-based routing and guardrails.
    - **server**: Derived from the running proxy's ``server_host``
      / ``server_port`` when available, avoiding the misleading
      ``127.0.0.1:0`` placeholder.
    - **x-forwarded-for**: Injected from ``client_ip`` if the
      original headers don't already carry it, as a fallback for
      IP attribution.
    """
    from fastapi import Request

    # --- Build ASGI headers ---
    _scope_headers: list = [(b"content-type", b"application/json")]
    # Hop-by-hop headers that must NOT be forwarded into the
    # synthetic request (they describe the original HTTP framing,
    # not the logical request).
    _HOP_BY_HOP = frozenset(
        {
            "content-length",
            "transfer-encoding",
            "connection",
            "keep-alive",
            "upgrade",
            "te",
            "trailer",
        }
    )
    if raw_headers:
        for hdr_name, hdr_value in raw_headers.items():
            _key = hdr_name.lower()
            # Skip content-type (already set), x-forwarded-for (use resolved
            # client_ip instead to prevent spoofing), and hop-by-hop headers
            if _key in {"content-type", "x-forwarded-for"} or _key in _HOP_BY_HOP:
                continue
            _scope_headers.append(
                (
                    _key.encode("latin-1", errors="replace"),
                    hdr_value.encode("utf-8"),
                )
            )

    # Inject x-forwarded-for from captured client_ip if the
    # original headers don't already carry it
    if client_ip and not any(h[0] == b"x-forwarded-for" for h in _scope_headers):
        _scope_headers.append((b"x-forwarded-for", client_ip.encode("utf-8")))

    # --- Derive server (host, port) from the running proxy ---
    _server_host = "127.0.0.1"
    _server_port = 4000  # LiteLLM default
    try:
        import litellm.proxy.proxy_server as proxy_server

        _proxy_host = getattr(proxy_server, "server_host", None)
        _proxy_port = getattr(proxy_server, "server_port", None)

        if _proxy_host:
            _server_host = str(_proxy_host)
        if _proxy_port:
            _server_port = int(_proxy_port)
    except (ImportError, AttributeError, TypeError, ValueError):
        pass

    # --- Build ASGI client tuple for request.client.host ---
    _client_tuple = None
    if client_ip:
        _client_tuple = (client_ip, 0)

    scope: Dict[str, Any] = {
        "type": "http",
        "method": "POST",
        "path": "/mcp/sampling/createMessage",
        "scheme": "http",
        "server": (_server_host, _server_port),
        "query_string": b"",
        "root_path": "",
        "headers": _scope_headers,
    }
    if _client_tuple is not None:
        scope["client"] = _client_tuple

    return Request(scope=scope)

