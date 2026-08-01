
def get_oidc_token(*, provider: Provider | str | None = None, audience: str | None = None) -> str:
    """Mint a raw OIDC id token (JWT) from the current CI provider.

    Args:
        provider (`str`, *optional*):
            CI provider to use. Auto-detected from the environment when omitted.
        audience (`str`, *optional*):
            The `aud` claim to request. Defaults to `constants.ENDPOINT` so it matches the endpoint
            that validates it (respects `HF_ENDPOINT`/staging).

    Returns:
        `str`: The raw id token (JWT) to pass to [`exchange_oidc_token`].
    """
    audience = audience or constants.ENDPOINT
    provider = provider or detect_provider()
    supported = ", ".join(p.value for p in Provider)
    if provider is None:
        raise OIDCError(f"No supported CI OIDC provider detected. Trusted Publishers currently supports: {supported}.")
    if provider == Provider.GITHUB:
        return _get_github_oidc_token(audience)
    raise NotImplementedError(f"OIDC provider '{provider}' is not supported yet. Supported: {supported}.")

