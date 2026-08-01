
def parse_set_cookie_headers(headers: Sequence[str]) -> list[tuple[str, Morsel[str]]]:
    """
    Parse cookie headers using a vendored version of SimpleCookie parsing.

    This implementation is based on SimpleCookie.__parse_string to ensure
    compatibility with how SimpleCookie parses cookies, including handling
    of malformed cookies with missing semicolons.

    This function is used for both Cookie and Set-Cookie headers in order to be
    forgiving. Ideally we would have followed RFC 6265 Section 5.2 (for Cookie
    headers) and RFC 6265 Section 4.2.1 (for Set-Cookie headers), but the
    real world data makes it impossible since we need to be a bit more forgiving.

    NOTE: This implementation differs from SimpleCookie in handling unmatched quotes.
    SimpleCookie will stop parsing when it encounters a cookie value with an unmatched
    quote (e.g., 'cookie="value'), causing subsequent cookies to be silently dropped.
    This implementation handles unmatched quotes more gracefully to prevent cookie loss.
    See https://github.com/aio-libs/aiohttp/issues/7993
    """
    parsed_cookies: list[tuple[str, Morsel[str]]] = []

    for header in headers:
        if not header:
            continue

        # Parse cookie string using SimpleCookie's algorithm
        i = 0
        n = len(header)
        current_morsel: Morsel[str] | None = None
        morsel_seen = False

        while 0 <= i < n:
            # Start looking for a cookie
            match = _COOKIE_PATTERN.match(header, i)
            if not match:
                # No more cookies
                break

            key, value = match.group("key"), match.group("val")
            i = match.end(0)
            lower_key = key.lower()

            if key[0] == "$":
                if not morsel_seen:
                    # We ignore attributes which pertain to the cookie
                    # mechanism as a whole, such as "$Version".
                    continue
                # Process as attribute
                if current_morsel is not None:
                    attr_lower_key = lower_key[1:]
                    if attr_lower_key in _COOKIE_KNOWN_ATTRS:
                        current_morsel[attr_lower_key] = value or ""
            elif lower_key in _COOKIE_KNOWN_ATTRS:
                if not morsel_seen:
                    # Invalid cookie string - attribute before cookie
                    break
                if lower_key in _COOKIE_BOOL_ATTRS:
                    # Boolean attribute with any value should be True
                    if current_morsel is not None and current_morsel.isReservedKey(key):
                        current_morsel[lower_key] = True
                elif value is None:
                    # Invalid cookie string - non-boolean attribute without value
                    break
                elif current_morsel is not None:
                    # Regular attribute with value
                    current_morsel[lower_key] = _unquote(value)
            elif value is not None:
                # This is a cookie name=value pair
                # Validate the name
                if key in _COOKIE_KNOWN_ATTRS or not _COOKIE_NAME_RE.match(key):
                    internal_logger.warning(
                        "Can not load cookies: Illegal cookie name %r", key
                    )
                    current_morsel = None
                else:
                    # Create new morsel
                    current_morsel = Morsel()
                    # Preserve the original value as coded_value (with quotes if present)
                    try:
                        current_morsel.__setstate__(  # type: ignore[attr-defined]
                            {
                                "key": key,
                                "value": _unquote(value),
                                "coded_value": value,
                            }
                        )
                    except CookieError:
                        current_morsel = None
                    else:
                        parsed_cookies.append((key, current_morsel))
                        morsel_seen = True
            else:
                # Invalid cookie string - no value for non-attribute
                break

    return parsed_cookies

