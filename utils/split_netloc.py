
def split_netloc(
    netloc: str,
) -> tuple[str | None, str | None, str | None, int | None]:
    """Split netloc into username, password, host and port."""
    if "@" not in netloc:
        username: str | None = None
        password: str | None = None
        hostinfo = netloc
    else:
        userinfo, _, hostinfo = netloc.rpartition("@")
        username, have_password, password = userinfo.partition(":")
        if not have_password:
            password = None

    if "[" in hostinfo:
        if hostinfo[0] != "[" or hostinfo.count("[") > 1 or hostinfo.count("]") > 1:
            raise ValueError("Invalid IPv6 URL")
        _, _, bracketed = hostinfo.partition("[")
        hostname, _, port_str = bracketed.partition("]")
        # Defense-in-depth: after ']' only ':port' or empty is valid.
        # split_url() should have already rejected invalid suffixes,
        # but guard here too for callers that use split_netloc() directly.
        if port_str and port_str[0] != ":":
            raise ValueError("Invalid IPv6 URL")
        _, _, port_str = port_str.partition(":")
    else:
        hostname, _, port_str = hostinfo.partition(":")

    if not port_str:
        return username or None, password, hostname or None, None

    try:
        port = int(port_str)
    except ValueError:
        raise ValueError("Invalid URL: port can't be converted to integer")
    if not (0 <= port <= 65535):
        raise ValueError("Port out of range 0-65535")
    return username or None, password, hostname or None, port

