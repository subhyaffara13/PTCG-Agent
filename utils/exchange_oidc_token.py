
def exchange_oidc_token(*, subject_token: str, resource: str, endpoint: str | None = None) -> dict:
    """Exchange a CI OIDC id token for a short-lived Hugging Face token (RFC 8693).

    Args:
        subject_token (`str`):
            The raw OIDC id token (JWT) from the CI provider. Its `aud` claim must be the Hub URL.
        resource (`str`):
            What to scope the token to: a Hub repo (`namespace/name`, `datasets/namespace/name`,
            `spaces/namespace/name`, `kernels/namespace/name`) for a write token, or a bare Hub
            username for a read-only `gated-repos` token.
        endpoint (`str`, *optional*):
            Hub endpoint. Defaults to `constants.ENDPOINT` (respects `HF_ENDPOINT`/staging).

    Returns:
        `dict`: The token-exchange response, e.g.
        `{"access_token": "hf_jwt_…", "token_type": "bearer", "expires_in": 3600, ...}`.
    """
    response = get_session().post(
        f"{endpoint or constants.ENDPOINT}/oauth/token",
        json={
            "grant_type": _TOKEN_EXCHANGE_GRANT_TYPE,
            "subject_token_type": _ID_TOKEN_TYPE,
            "subject_token": subject_token,
            "resource": resource,
        },
    )
    hf_raise_for_status(response)
    return response.json()

