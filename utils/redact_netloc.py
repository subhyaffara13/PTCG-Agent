
def redact_netloc(netloc: str) -> str:
    """
    Replace the sensitive data in a netloc with "****", if it exists.

    For example:
        - "user:pass@example.com" returns "user:****@example.com"
        - "accesstoken@example.com" returns "****@example.com"
    """
    netloc, (user, password) = split_auth_from_netloc(netloc)
    if user is None:
        return netloc
    if password is None:
        user = "****"
        password = ""
    else:
        user = urllib.parse.quote(user)
        password = ":****"
    return f"{user}{password}@{netloc}"

