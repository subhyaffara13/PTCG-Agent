
def refresh_access_token(refresh_token: str) -> OAuthTokenResponse:
    """Exchange a refresh token for a new access token.

    Returns:
        `OAuthTokenResponse`: the full token response: `access_token`, and optionally a rotated
        `refresh_token` and `expires_in`.

    Raises:
        [`DeviceCodeError`]: If the server rejects the refresh (`error_code="invalid_grant"` when
            the refresh token is expired or revoked) or returns an unexpected response.
    """
    try:
        response = get_session().post(
            f"{constants.ENDPOINT}/oauth/token",
            data={
                "grant_type": _REFRESH_TOKEN_GRANT_TYPE,
                "refresh_token": refresh_token,
                "client_id": constants.DEVICE_CODE_OAUTH_CLIENT_ID,
            },
            # An explicit timeout is critical here: this runs inside `get_token()`, so a hung
            # request would otherwise block every Hub call in the process.
            timeout=constants.HF_HUB_DOWNLOAD_TIMEOUT,
        )
    except httpx.HTTPError as e:
        raise DeviceCodeError(f"Failed to refresh access token: {e}") from e
    data = _parse_token_response(response)
    if "access_token" in data:
        return cast(OAuthTokenResponse, data)
    error = data.get("error")
    raise DeviceCodeError(
        f"Failed to refresh access token: {error or response.status_code} - {data.get('error_description', '')}",
        error_code=error,
    )

