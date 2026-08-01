
def _parse_expiry(response_data):
    """Parses the expiry field from a response into a datetime.

    Args:
        response_data (Mapping): The JSON-parsed response data.

    Returns:
        Optional[datetime]: The expiration or ``None`` if no expiration was
            specified.
    """
    expires_in = response_data.get("expires_in", None)

    if expires_in is not None:
        # Some services do not respect the OAUTH2.0 RFC and send expires_in as a
        # JSON String.
        if isinstance(expires_in, str):
            expires_in = int(expires_in)

        return _helpers.utcnow() + datetime.timedelta(seconds=expires_in)
    else:
        return None

