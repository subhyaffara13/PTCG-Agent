
def get_rapt_token(
    request, client_id, client_secret, refresh_token, token_uri, scopes=None
):
    """Given an http request method and refresh_token, get rapt token.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        client_id (str): client id to get access token for reauth scope.
        client_secret (str): client secret for the client_id
        refresh_token (str): refresh token to refresh access token
        token_uri (str): uri to refresh access token
        scopes (Optional(Sequence[str])): scopes required by the client application

    Returns:
        str: The rapt token.
    Raises:
        google.auth.exceptions.RefreshError: If reauth failed.
    """
    sys.stderr.write("Reauthentication required.\n")

    # Get access token for reauth.
    access_token, _, _, _ = _client.refresh_grant(
        request=request,
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        token_uri=token_uri,
        scopes=[_REAUTH_SCOPE],
    )

    # Get rapt token from reauth API.
    rapt_token = _obtain_rapt(request, access_token, requested_scopes=scopes)
    sys.stderr.write("Reauthentication successful.\n")

    return rapt_token

