
def call_iam_generate_id_token_endpoint(
    request,
    iam_id_token_endpoint,
    signer_email,
    audience,
    access_token,
    universe_domain=credentials.DEFAULT_UNIVERSE_DOMAIN,
):
    """Call iam.generateIdToken endpoint to get ID token.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        iam_id_token_endpoint (str): The IAM ID token endpoint to use.
        signer_email (str): The signer email used to form the IAM
            generateIdToken endpoint.
        audience (str): The audience for the ID token.
        access_token (str): The access token used to call the IAM endpoint.
        universe_domain (str): The universe domain for the request. The
            default is ``googleapis.com``.

    Returns:
        Tuple[str, datetime]: The ID token and expiration.
    """
    body = {"audience": audience, "includeEmail": "true", "useEmailAzp": "true"}

    response_data = _token_endpoint_request(
        request,
        iam_id_token_endpoint.replace(
            credentials.DEFAULT_UNIVERSE_DOMAIN, universe_domain
        ).format(signer_email),
        body,
        access_token=access_token,
        use_json=True,
    )

    try:
        id_token = response_data["token"]
    except KeyError as caught_exc:
        new_exc = exceptions.RefreshError(
            "No ID token in response.", response_data, retryable=False
        )
        raise new_exc from caught_exc

    payload = jwt.decode(id_token, verify=False)
    expiry = _helpers.utcfromtimestamp(payload["exp"])

    return id_token, expiry

