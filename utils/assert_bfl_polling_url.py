
def assert_bfl_polling_url(polling_url: str) -> None:
    """Validate that a polling URL points to a BFL-controlled host.

    BFL returns polling URLs on subdomains like ``gateway.bfl.ai`` that differ
    from the submission host ``api.bfl.ai``. A strict same-origin check would
    reject these legitimate URLs. Instead we verify the host is ``bfl.ai`` or
    any subdomain of it, which keeps the SSRF guarantee (credentials only go
    to BFL-controlled infrastructure) without false-positives on regional hosts.

    Raises:
        BlackForestLabsError: If the polling URL scheme or host is not trusted.
    """
    parsed = urlparse(polling_url)
    host = (parsed.hostname or "").lower()

    if parsed.scheme != "https":
        raise BlackForestLabsError(
            status_code=502,
            message="Rejected polling URL: scheme must be https",
        )

    if host != _BFL_REGISTERED_DOMAIN and not host.endswith(
        "." + _BFL_REGISTERED_DOMAIN
    ):
        raise BlackForestLabsError(
            status_code=502,
            message="Rejected polling URL: host is not within the bfl.ai domain",
        )

