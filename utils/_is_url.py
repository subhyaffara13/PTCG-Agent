
def _is_url(name):
    scheme = _get_url_scheme(name)
    if scheme is None:
        return False
    return scheme in ["http", "https", "file", "ftp"] + VCS_SCHEMES


def _is_url(s: str) -> bool:
    return bool(_SCHEME_RE.match(s))

