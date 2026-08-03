from typing import Any, Union

def verify_token(
    id_token: Union[str, bytes],
    request: transport.Request,
    audience: Union[str, list[str], None] = None,
    certs_url: str = _GOOGLE_OAUTH2_CERTS_URL,
    clock_skew_in_seconds: int = 0,
) -> Mapping[str, Any]:
    """Verifies an ID token and returns the decoded token.

    Args:
        id_token (Union[str, bytes]): The encoded token.
        request (google.auth.transport.Request): The object used to make
            HTTP requests.
        audience (str or list): The audience or audiences that this token is
            intended for. If None then the audience is not verified.
        certs_url (str): The URL that specifies the certificates to use to
            verify the token. This URL should return JSON in the format of
            ``{'key id': 'x509 certificate'}`` or a certificate array according to
            the JWK spec (see https://tools.ietf.org/html/rfc7517).
        clock_skew_in_seconds (int): The clock skew used for `iat` and `exp`
            validation.

    Returns:
        Mapping[str, Any]: The decoded token.
    """
    certs = _fetch_certs(request, certs_url)

    if "keys" in certs:
        try:
            import jwt as jwt_lib  # type: ignore
        except ImportError as caught_exc:  # pragma: NO COVER
            raise ImportError(
                "The pyjwt library is not installed, please install the pyjwt package to use the jwk certs format."
            ) from caught_exc
        jwks_client = jwt_lib.PyJWKClient(certs_url)
        signing_key = jwks_client.get_signing_key_from_jwt(id_token)
        return jwt_lib.decode(
            id_token,
            signing_key.key,
            algorithms=[signing_key.algorithm_name],
            audience=audience,
        )
    else:
        return jwt.decode(
            id_token,
            certs=certs,
            audience=audience,
            clock_skew_in_seconds=clock_skew_in_seconds,
        )

