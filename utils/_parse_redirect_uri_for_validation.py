
def _parse_redirect_uri_for_validation(redirect_uri: str) -> ParseResult:
    try:
        return urlparse(redirect_uri)
    except ValueError:
        _oauth_invalid_request(
            "redirect_uri is not a valid URL.",
            hint="Use a full absolute URL for redirect_uri (e.g. https://your-host/ui/mcp/oauth/callback).",
        )

