
def get_file_content(filename: str) -> str:
    """
    Return the unicode text content of a filename.
    Respects # -*- coding: declarations on the retrieved files.

    :param filename:         File path.
    """
    try:
        with open(filename, "rb") as f:
            content = auto_decode(f.read())
    except OSError as exc:
        raise InstallationError(
            f"Could not open requirements file: {filename}|n{exc}"
        )
    return content


def get_file_content(
    url: str, session: PipSession, *, constraint: bool = False
) -> tuple[str, str]:
    """Gets the content of a file; it may be a filename, file: URL, or
    http: URL.  Returns (location, content).  Content is unicode.
    Respects # -*- coding: declarations on the retrieved files.

    :param url:         File path or url.
    :param session:     PipSession instance.
    """
    scheme = urllib.parse.urlsplit(url).scheme
    # Pip has special support for file:// URLs (LocalFSAdapter).
    if scheme in ["http", "https", "file"]:
        # Delay importing heavy network modules until absolutely necessary.
        from pip._internal.network.utils import raise_for_status

        resp = session.get(url)
        raise_for_status(resp)
        return resp.url, resp.text

    # Assume this is a bare path.
    try:
        with open(url, "rb") as f:
            raw_content = f.read()
    except OSError as exc:
        kind = "constraint" if constraint else "requirements"
        raise InstallationError(f"Could not open {kind} file: {exc}")

    content = _decode_req_file(raw_content, url)

    return url, content

