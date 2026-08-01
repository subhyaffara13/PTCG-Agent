
def preserve_morsel_with_coded_value(cookie: Morsel[str]) -> Morsel[str]:
    """
    Preserve a Morsel's coded_value exactly as received from the server.

    This function ensures that cookie encoding is preserved exactly as sent by
    the server, which is critical for compatibility with old servers that have
    strict requirements about cookie formats.

    This addresses the issue described in https://github.com/aio-libs/aiohttp/pull/1453
    where Python's SimpleCookie would re-encode cookies, breaking authentication
    with certain servers.

    Args:
        cookie: A Morsel object from SimpleCookie

    Returns:
        A Morsel object with preserved coded_value

    """
    mrsl_val = cast("Morsel[str]", cookie.get(cookie.key, Morsel()))
    # We use __setstate__ instead of the public set() API because it allows us to
    # bypass validation and set already validated state. This is more stable than
    # setting protected attributes directly and unlikely to change since it would
    # break pickling.
    try:
        mrsl_val.__setstate__(  # type: ignore[attr-defined]
            {
                "key": cookie.key,
                "value": cookie.value,
                "coded_value": cookie.coded_value,
            }
        )
    except CookieError:
        return cookie
    return mrsl_val

