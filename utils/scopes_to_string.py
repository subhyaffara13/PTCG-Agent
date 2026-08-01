
def scopes_to_string(scopes):
    """Converts scope value to a string suitable for sending to OAuth 2.0
    authorization servers.

    Args:
        scopes (Sequence[str]): The sequence of scopes to convert.

    Returns:
        str: The scopes formatted as a single string.
    """
    return " ".join(scopes)

