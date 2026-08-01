
def xet_headers_without_auth(headers: dict[str, str]) -> dict[str, str]:
    """Return a copy of headers with the authorization header removed.

    Xet storage requests use a short-lived xet access token for auth, so the
    Hub authorization header must not be forwarded to xet storage endpoints.
    """
    return {key: value for key, value in headers.items() if key.lower() != "authorization"}

