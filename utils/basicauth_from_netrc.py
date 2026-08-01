
def basicauth_from_netrc(netrc_obj: netrc.netrc | None, host: str) -> BasicAuth:
    """
    Return :py:class:`~aiohttp.BasicAuth` credentials for ``host`` from ``netrc_obj``.

    :raises LookupError: if ``netrc_obj`` is :py:data:`None` or if no
            entry is found for the ``host``.
    """
    if netrc_obj is None:
        raise LookupError("No .netrc file found")
    auth_from_netrc = netrc_obj.authenticators(host)

    if auth_from_netrc is None:
        raise LookupError(f"No entry for {host!s} found in the `.netrc` file.")
    login, account, password = auth_from_netrc

    # TODO(PY311): username = login or account
    # Up to python 3.10, account could be None if not specified,
    # and login will be empty string if not specified. From 3.11,
    # login and account will be empty string if not specified.
    username = login if (login or account is None) else account

    # TODO(PY311): Remove this, as password will be empty string
    # if not specified
    if password is None:
        password = ""

    return _basic_auth_no_warn(username, password)

