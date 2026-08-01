
def refresh_grant(
    request,
    token_uri,
    refresh_token,
    client_id,
    client_secret,
    scopes=None,
    rapt_token=None,
    enable_reauth_refresh=False,
):
    """Implements the reauthentication flow.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        token_uri (str): The OAuth 2.0 authorizations server's token endpoint
            URI.
        refresh_token (str): The refresh token to use to get a new access
            token.
        client_id (str): The OAuth 2.0 application's client ID.
        client_secret (str): The Oauth 2.0 appliaction's client secret.
        scopes (Optional(Sequence[str])): Scopes to request. If present, all
            scopes must be authorized for the refresh token. Useful if refresh
            token has a wild card scope (e.g.
            'https://www.googleapis.com/auth/any-api').
        rapt_token (Optional(str)): The rapt token for reauth.
        enable_reauth_refresh (Optional[bool]): Whether reauth refresh flow
            should be used. The default value is False. This option is for
            gcloud only, other users should use the default value.

    Returns:
        Tuple[str, Optional[str], Optional[datetime], Mapping[str, str], str]: The
            access token, new refresh token, expiration, the additional data
            returned by the token endpoint, and the rapt token.

    Raises:
        google.auth.exceptions.RefreshError: If the token endpoint returned
            an error.
    """
    body = {
        "grant_type": _client._REFRESH_GRANT_TYPE,
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }
    if scopes:
        body["scope"] = " ".join(scopes)
    if rapt_token:
        body["rapt"] = rapt_token
    metrics_header = {metrics.API_CLIENT_HEADER: metrics.token_request_user()}

    (
        response_status_ok,
        response_data,
        retryable_error,
    ) = _client._token_endpoint_request_no_throw(
        request, token_uri, body, headers=metrics_header
    )

    if not response_status_ok and isinstance(response_data, str):
        raise exceptions.RefreshError(response_data, retryable=False)

    if (
        not response_status_ok
        and response_data.get("error") == _REAUTH_NEEDED_ERROR
        and (
            response_data.get("error_subtype") == _REAUTH_NEEDED_ERROR_INVALID_RAPT
            or response_data.get("error_subtype") == _REAUTH_NEEDED_ERROR_RAPT_REQUIRED
        )
    ):
        if not enable_reauth_refresh:
            raise exceptions.RefreshError(
                "Reauthentication is needed. Please run `gcloud auth application-default login` to reauthenticate."
            )

        rapt_token = get_rapt_token(
            request, client_id, client_secret, refresh_token, token_uri, scopes=scopes
        )
        body["rapt"] = rapt_token
        (
            response_status_ok,
            response_data,
            retryable_error,
        ) = _client._token_endpoint_request_no_throw(
            request, token_uri, body, headers=metrics_header
        )

    if not response_status_ok:
        _client._handle_error_response(response_data, retryable_error)
    return _client._handle_refresh_grant_response(response_data, refresh_token) + (
        rapt_token,
    )


def refresh_grant(
    request,
    token_uri,
    refresh_token,
    client_id,
    client_secret,
    scopes=None,
    rapt_token=None,
    can_retry=True,
):
    """Implements the OAuth 2.0 refresh token grant.

    For more details, see `rfc678 section 6`_.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        token_uri (str): The OAuth 2.0 authorizations server's token endpoint
            URI.
        refresh_token (str): The refresh token to use to get a new access
            token.
        client_id (str): The OAuth 2.0 application's client ID.
        client_secret (str): The Oauth 2.0 appliaction's client secret.
        scopes (Optional(Sequence[str])): Scopes to request. If present, all
            scopes must be authorized for the refresh token. Useful if refresh
            token has a wild card scope (e.g.
            'https://www.googleapis.com/auth/any-api').
        rapt_token (Optional(str)): The reauth Proof Token.
        can_retry (bool): Enable or disable request retry behavior.

    Returns:
        Tuple[str, str, Optional[datetime], Mapping[str, str]]: The access
            token, new or current refresh token, expiration, and additional data
            returned by the token endpoint.

    Raises:
        google.auth.exceptions.RefreshError: If the token endpoint returned
            an error.

    .. _rfc6748 section 6: https://tools.ietf.org/html/rfc6749#section-6
    """
    body = {
        "grant_type": _REFRESH_GRANT_TYPE,
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }
    if scopes:
        body["scope"] = " ".join(scopes)
    if rapt_token:
        body["rapt"] = rapt_token

    response_data = _token_endpoint_request(
        request, token_uri, body, can_retry=can_retry
    )
    return _handle_refresh_grant_response(response_data, refresh_token)

