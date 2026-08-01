
def _raise_trusted_redirect_uri_rejected(
    request: Request,
    redirect_uri: str,
    parsed: ParseResult,
    redirect_netloc: str,
    proxy_base: Optional[str],
) -> NoReturn:
    description = _build_trusted_redirect_rejection_message(
        redirect_uri, parsed, redirect_netloc, proxy_base
    )

    hint = (
        "Align the proxy public URL with the browser URL. Set PROXY_BASE_URL to your "
        "HTTPS origin (e.g. https://litellm.example.com), or enable "
        "general_settings.use_x_forwarded_for with mcp_trusted_proxy_ranges for your "
        "ingress. Verify: curl https://<host>/.well-known/oauth-authorization-server "
        "| jq .issuer — issuer must match window.location.origin in the UI."
    )

    verbose_logger.warning(
        "MCP OAuth: rejecting redirect_uri %r. %s "
        "Computed proxy base=%r (PROXY_BASE_URL=%r). "
        "Inbound headers: X-Forwarded-Proto=%r X-Forwarded-Host=%r "
        "X-Forwarded-Port=%r Host=%r. "
        "Trusted-redirect-origins env=%r. "
        "Trusted-native-redirect-uris env=%r.",
        redirect_uri,
        description,
        proxy_base,
        os.environ.get("PROXY_BASE_URL"),
        request.headers.get("X-Forwarded-Proto"),
        request.headers.get("X-Forwarded-Host"),
        request.headers.get("X-Forwarded-Port"),
        request.headers.get("Host"),
        os.environ.get(_TRUSTED_REDIRECT_ORIGINS_ENV),
        os.environ.get(_TRUSTED_NATIVE_REDIRECT_URIS_ENV),
    )

    _oauth_invalid_request(
        description,
        hint=hint,
        redirect_uri=redirect_uri,
    )

