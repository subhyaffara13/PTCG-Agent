
def _sign_jwt_request(request, principal, headers, payload, delegates=[]):
    """Makes a request to the Google Cloud IAM service to sign a JWT using a
    service account's system-managed private key.
    Args:
        request (Request): The Request object to use.
        principal (str): The principal to request an access token for.
        headers (Mapping[str, str]): Map of headers to transmit.
        payload (Mapping[str, str]): The JWT payload to sign. Must be a
            serialized JSON object that contains a JWT Claims Set.
        delegates (Sequence[str]): The chained list of delegates required
            to grant the final access_token.  If set, the sequence of
            identities must have "Service Account Token Creator" capability
            granted to the prceeding identity.  For example, if set to
            [serviceAccountB, serviceAccountC], the source_credential
            must have the Token Creator role on serviceAccountB.
            serviceAccountB must have the Token Creator on
            serviceAccountC.
            Finally, C must have Token Creator on target_principal.
            If left unset, source_credential must have that role on
            target_principal.

    Raises:
        google.auth.exceptions.TransportError: Raised if there is an underlying
            HTTP connection error
        google.auth.exceptions.RefreshError: Raised if the impersonated
            credentials are not available.  Common reasons are
            `iamcredentials.googleapis.com` is not enabled or the
            `Service Account Token Creator` is not assigned
    """
    iam_endpoint = iam._IAM_SIGNJWT_ENDPOINT.format(principal)

    body = {"delegates": delegates, "payload": json.dumps(payload)}
    body = json.dumps(body).encode("utf-8")

    response = request(url=iam_endpoint, method="POST", headers=headers, body=body)

    # support both string and bytes type response.data
    response_body = (
        response.data.decode("utf-8")
        if hasattr(response.data, "decode")
        else response.data
    )

    if response.status != http_client.OK:
        raise exceptions.RefreshError(_REFRESH_ERROR, response_body)

    try:
        jwt_response = json.loads(response_body)
        signed_jwt = jwt_response["signedJwt"]
        return signed_jwt

    except (KeyError, ValueError) as caught_exc:
        new_exc = exceptions.RefreshError(
            "{}: No signed JWT in response.".format(_REFRESH_ERROR), response_body
        )
        raise new_exc from caught_exc

