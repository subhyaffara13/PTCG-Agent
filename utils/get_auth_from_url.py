
def get_auth_from_url(url: str) -> tuple[str, str]:
    """Given a url with authentication components, extract them into a tuple of
    username,password.

    :rtype: (str,str)
    """
    parsed = urlparse(url)

    try:
        # except handles parsed.username/password being None
        auth = (unquote(parsed.username), unquote(parsed.password))  # type: ignore[arg-type]
    except (AttributeError, TypeError):
        auth = ("", "")

    return auth


def get_auth_from_url(url):
    """Given a url with authentication components, extract them into a tuple of
    username,password.

    :rtype: (str,str)
    """
    parsed = urlparse(url)

    try:
        auth = (unquote(parsed.username), unquote(parsed.password))
    except (AttributeError, TypeError):
        auth = ("", "")

    return auth

