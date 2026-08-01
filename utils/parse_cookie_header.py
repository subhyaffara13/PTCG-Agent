
def parse_cookie_header(header: str) -> list[tuple[str, Morsel[str]]]:
    """
    Parse a Cookie header according to RFC 6265 Section 5.4.

    Cookie headers contain only name-value pairs separated by semicolons.
    There are no attributes in Cookie headers - even names that match
    attribute names (like 'path' or 'secure') should be treated as cookies.

    This parser uses the same regex-based approach as parse_set_cookie_headers
    to properly handle quoted values that may contain semicolons. When the
    regex fails to match a malformed cookie, it falls back to simple parsing
    to ensure subsequent cookies are not lost
    https://github.com/aio-libs/aiohttp/issues/11632

    Args:
        header: The Cookie header value to parse

    Returns:
        List of (name, Morsel) tuples for compatibility with SimpleCookie.update()
    """
    if not header:
        return []

    cookies: list[tuple[str, Morsel[str]]] = []
    morsel: Morsel[str]
    i = 0
    n = len(header)

    invalid_names = []
    while i < n:
        # Use the same pattern as parse_set_cookie_headers to find cookies
        match = _COOKIE_PATTERN.match(header, i)
        if not match:
            # Fallback for malformed cookies https://github.com/aio-libs/aiohttp/issues/11632
            # Find next semicolon to skip or attempt simple key=value parsing
            next_semi = header.find(";", i)
            eq_pos = header.find("=", i)

            # Try to extract key=value if '=' comes before ';'
            if eq_pos != -1 and (next_semi == -1 or eq_pos < next_semi):
                end_pos = next_semi if next_semi != -1 else n
                key = header[i:eq_pos].strip()
                value = header[eq_pos + 1 : end_pos].strip()

                # Validate the name (same as regex path)
                if not _COOKIE_NAME_RE.match(key):
                    invalid_names.append(key)
                else:
                    morsel = Morsel()
                    try:
                        morsel.__setstate__(  # type: ignore[attr-defined]
                            {
                                "key": key,
                                "value": _unquote(value),
                                "coded_value": value,
                            }
                        )
                    except CookieError:
                        pass
                    else:
                        cookies.append((key, morsel))

            # Move to next cookie or end
            i = next_semi + 1 if next_semi != -1 else n
            continue

        key = match.group("key")
        value = match.group("val") or ""
        i = match.end(0)

        # Validate the name
        if not key or not _COOKIE_NAME_RE.match(key):
            invalid_names.append(key)
            continue

        # Create new morsel
        morsel = Morsel()
        # Preserve the original value as coded_value (with quotes if present)
        # We use __setstate__ instead of the public set() API because it allows us to
        # bypass validation and set already validated state. This is more stable than
        # setting protected attributes directly and unlikely to change since it would
        # break pickling.
        try:
            morsel.__setstate__(  # type: ignore[attr-defined]
                {"key": key, "value": _unquote(value), "coded_value": value}
            )
        except CookieError:
            continue

        cookies.append((key, morsel))

    if invalid_names:
        internal_logger.debug(
            "Cannot load cookie. Illegal cookie names: %r", invalid_names
        )

    return cookies

