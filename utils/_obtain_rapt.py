
def _obtain_rapt(request, access_token, requested_scopes):
    """Given an http request method and reauth access token, get rapt token.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        access_token (str): reauth access token
        requested_scopes (Sequence[str]): scopes required by the client application

    Returns:
        str: The rapt token.

    Raises:
        google.auth.exceptions.ReauthError: if reauth failed
    """
    msg = _get_challenges(
        request,
        list(challenges.AVAILABLE_CHALLENGES.keys()),
        access_token,
        requested_scopes,
    )

    if msg["status"] == _AUTHENTICATED:
        return msg["encodedProofOfReauthToken"]

    for _ in range(0, RUN_CHALLENGE_RETRY_LIMIT):
        if not (
            msg["status"] == _CHALLENGE_REQUIRED or msg["status"] == _CHALLENGE_PENDING
        ):
            raise exceptions.ReauthFailError(
                "Reauthentication challenge failed due to API error: {}".format(
                    msg["status"]
                )
            )

        if not is_interactive():
            raise exceptions.ReauthFailError(
                "Reauthentication challenge could not be answered because you are not"
                " in an interactive session."
            )

        msg = _run_next_challenge(msg, request, access_token)

        if not msg:
            raise exceptions.ReauthFailError("Failed to obtain rapt token.")
        if msg["status"] == _AUTHENTICATED:
            return msg["encodedProofOfReauthToken"]

    # If we got here it means we didn't get authenticated.
    raise exceptions.ReauthFailError("Failed to obtain rapt token.")

