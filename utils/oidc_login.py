
def oidc_login(
    *,
    resource: str,
    subject_token: str | None = None,
    provider: Provider | str | None = None,
    audience: str | None = None,
    endpoint: str | None = None,
) -> dict:
    """Mint a CI OIDC id token and exchange it for a Hugging Face token.

    Convenience wrapper around [`get_oidc_token`] + [`exchange_oidc_token`]. Returns the raw
    exchange response (it does not persist anything — the caller decides what to do with the token).

    Args:
        resource (`str`):
            Repo or username to scope the token to. See [`exchange_oidc_token`].
        subject_token (`str`, *optional*):
            A pre-minted OIDC id token to exchange directly. Use this for CI providers not yet
            supported natively (e.g. GitLab): mint the id token in your job and pass it here. When
            omitted, the token is minted from the detected `provider`.
        provider (`str`, *optional*):
            CI provider. Auto-detected when omitted. Ignored when `subject_token` is provided.
        audience (`str`, *optional*):
            The `aud` claim to request. Defaults to the resolved `endpoint`, so it matches the
            endpoint that validates it.
        endpoint (`str`, *optional*):
            Hub endpoint. Defaults to `constants.ENDPOINT`.

    Returns:
        `dict`: The token-exchange response (`access_token`, `token_type`, `expires_in`, ...).
    """
    endpoint = endpoint or constants.ENDPOINT
    if subject_token is None:
        subject_token = get_oidc_token(provider=provider, audience=audience or endpoint)
    return exchange_oidc_token(subject_token=subject_token, resource=resource, endpoint=endpoint)

