import json

def _fetch_certs(request, certs_url):
    """Fetches certificates.

    Google-style certificate endpoints return JSON in the format of
    ``{'key id': 'x509 certificate'}`` or a certificate array according
    to the JWK spec (see https://tools.ietf.org/html/rfc7517).

    Args:
        request (google.auth.transport.Request): The object used to make
            HTTP requests.
        certs_url (str): The certificate endpoint URL.

    Returns:
        Mapping[str, str] | Mapping[str, list]: A mapping of public keys
        in x.509 or JWK spec.
    """
    response = request(certs_url, method="GET")

    if response.status != http_client.OK:
        raise exceptions.TransportError(
            "Could not fetch certificates at {}".format(certs_url)
        )

    return json.loads(response.data.decode("utf-8"))

