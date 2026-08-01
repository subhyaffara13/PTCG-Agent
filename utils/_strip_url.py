
def _strip_url(url: str, safe_user_passwords: Collection[str]) -> str:
    """url with user:password part removed unless it is formed with
    environment variables as specified in PEP 610, or it is a safe user:password
    such as `git`.
    """
    parsed_url = urllib.parse.urlsplit(url)
    netloc = _strip_auth_from_netloc(parsed_url.netloc, safe_user_passwords)
    return urllib.parse.urlunsplit(
        (
            parsed_url.scheme,
            netloc,
            parsed_url.path,
            parsed_url.query,
            parsed_url.fragment,
        )
    )


def _strip_url(url: str, safe_user_passwords: Collection[str]) -> str:
    """url with user:password part removed unless it is formed with
    environment variables as specified in PEP 610, or it is a safe user:password
    such as `git`.
    """
    parsed_url = urllib.parse.urlsplit(url)
    netloc = _strip_auth_from_netloc(parsed_url.netloc, safe_user_passwords)
    return urllib.parse.urlunsplit(
        (
            parsed_url.scheme,
            netloc,
            parsed_url.path,
            parsed_url.query,
            parsed_url.fragment,
        )
    )

