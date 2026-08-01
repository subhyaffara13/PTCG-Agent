
def encode_basic_auth(login: str, password: str = "", encoding: str = "utf-8") -> str:
    """Encode HTTP Basic Authentication credentials as an Authorization header value.

    Returns a string of the form ``"Basic <base64>"`` suitable for use as the
    value of the ``Authorization`` (or ``Proxy-Authorization``) header.
    """
    if ":" in login:
        raise ValueError('A ":" is not allowed in login (RFC 7617#section-2)')
    creds = f"{login}:{password}".encode(encoding)
    return "Basic " + base64.b64encode(creds).decode(encoding)

