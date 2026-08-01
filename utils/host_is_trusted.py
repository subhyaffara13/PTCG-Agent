
def host_is_trusted(
    hostname: str | None, trusted_list: t.Collection[str] | None = None
) -> bool:
    """Perform some checks on a ``Host`` header ``host:port``. The host must be
    made up of valid characters, but this does not check validity beyond that.
    If a list of trusted domains is given, the domain must match one.

    :param hostname: The ``Host`` header ``host:port`` to check.
    :param trusted_list: A list of trusted domains to match. These should
        already be IDNA encoded, but will be encoded if needed. The port is
        ignored for this check. If a name starts with a dot it will match as a
        suffix, accepting all subdomains. If empty or ``None``, all domains are
        allowed.

    .. versionchanged:: 3.2
        The value's characters are validated.

    .. versionchanged:: 3.2
        ``trusted_list`` defaults to ``None``.

    .. versionadded:: 0.9
    """
    if not hostname:
        return False

    if _host_re.fullmatch(hostname) is None:
        return False

    hostname = hostname.partition(":")[0]

    if not trusted_list:
        return True

    if isinstance(trusted_list, str):
        trusted_list = [trusted_list]

    for ref in trusted_list:
        if ref.startswith("."):
            ref = ref[1:]
            suffix_match = True
        else:
            suffix_match = False

        try:
            ref = ref.partition(":")[0].encode("idna").decode("ascii")
        except UnicodeEncodeError:
            return False

        if ref == hostname or (suffix_match and hostname.endswith(f".{ref}")):
            return True

    return False

