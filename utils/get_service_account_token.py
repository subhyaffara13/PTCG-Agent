
def get_service_account_token(request, service_account="default", scopes=None):
    """Get the OAuth 2.0 access token for a service account.

    Args:
        request (google.auth.transport.Request): A callable used to make
            HTTP requests.
        service_account (str): The string 'default' or a service account email
            address. The determines which service account for which to acquire
            an access token.
        scopes (Optional[Union[str, List[str]]]): Optional string or list of
            strings with auth scopes.
    Returns:
        Tuple[str, datetime]: The access token and its expiration.

    Raises:
        google.auth.exceptions.TransportError: if an error occurred while
            retrieving metadata.
    """
    from google.auth import _agent_identity_utils

    params = {}
    if scopes:
        if not isinstance(scopes, str):
            scopes = ",".join(scopes)
        params["scopes"] = scopes

    cert = _agent_identity_utils.get_and_parse_agent_identity_certificate()
    if cert:
        if _agent_identity_utils.should_request_bound_token(cert):
            fingerprint = _agent_identity_utils.calculate_certificate_fingerprint(cert)
            params["bindCertificateFingerprint"] = fingerprint

    metrics_header = {
        metrics.API_CLIENT_HEADER: metrics.token_request_access_token_mds()
    }

    path = "instance/service-accounts/{0}/token".format(service_account)
    token_json = get(request, path, params=params, headers=metrics_header)
    token_expiry = _helpers.utcnow() + datetime.timedelta(
        seconds=token_json["expires_in"]
    )
    return token_json["access_token"], token_expiry

