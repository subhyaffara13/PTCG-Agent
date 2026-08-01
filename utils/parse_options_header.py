
def parse_options_header(value: str | None) -> tuple[str, dict[str, str]]:
    """Parse a header that consists of a value with ``key=value`` parameters separated
    by semicolons ``;``. For example, the ``Content-Type`` header.

    .. code-block:: python

        parse_options_header("text/html; charset=UTF-8")
        ('text/html', {'charset': 'UTF-8'})

        parse_options_header("")
        ("", {})

    This is the reverse of :func:`dump_options_header`.

    This parses valid parameter parts as described in
    `RFC 9110 <https://httpwg.org/specs/rfc9110.html#parameter>`__. Invalid parts are
    skipped.

    This handles continuations and charsets as described in
    `RFC 2231 <https://www.rfc-editor.org/rfc/rfc2231#section-3>`__, although not as
    strictly as the RFC. Only ASCII, UTF-8, and ISO-8859-1 charsets are accepted,
    otherwise the value remains quoted.

    Clients may not be consistent in how they handle a quote character within a quoted
    value. The `HTML Standard <https://html.spec.whatwg.org/#multipart-form-data>`__
    replaces it with ``%22`` in multipart form data.
    `RFC 9110 <https://httpwg.org/specs/rfc9110.html#quoted.strings>`__ uses backslash
    escapes in HTTP headers. Both are decoded to the ``"`` character.

    Clients may not be consistent in how they handle non-ASCII characters. HTML
    documents must declare ``<meta charset=UTF-8>``, otherwise browsers may replace with
    HTML character references, which can be decoded using :func:`html.unescape`.

    :param value: The header value to parse.
    :return: ``(value, options)``, where ``options`` is a dict

    .. versionchanged:: 2.3
        Invalid parts, such as keys with no value, quoted keys, and incorrectly quoted
        values, are discarded instead of treating as ``None``.

    .. versionchanged:: 2.3
        Only ASCII, UTF-8, and ISO-8859-1 are accepted for charset values.

    .. versionchanged:: 2.3
        Escaped quotes in quoted values, like ``%22`` and ``\\"``, are handled.

    .. versionchanged:: 2.2
        Option names are always converted to lowercase.

    .. versionchanged:: 2.2
        The ``multiple`` parameter was removed.

    .. versionchanged:: 0.15
        :rfc:`2231` parameter continuations are handled.

    .. versionadded:: 0.5
    """
    if value is None:
        return "", {}

    value, _, rest = value.partition(";")
    value = value.strip()
    rest = rest.strip()

    if not value or not rest:
        # empty (invalid) value, or value without options
        return value, {}

    # Collect all valid key=value parts without processing the value.
    parts: list[tuple[str, str]] = []

    while True:
        if (m := _parameter_key_re.match(rest)) is not None:
            pk = m.group(1).lower()
            rest = rest[m.end() :]

            # Value may be a token.
            if (m := _parameter_token_value_re.match(rest)) is not None:
                parts.append((pk, m.group()))

            # Value may be a quoted string, find the closing quote.
            elif rest[:1] == '"':
                pos = 1
                length = len(rest)

                while pos < length:
                    if rest[pos : pos + 2] in {"\\\\", '\\"'}:
                        # Consume escaped slashes and quotes.
                        pos += 2
                    elif rest[pos] == '"':
                        # Stop at an unescaped quote.
                        parts.append((pk, rest[: pos + 1]))
                        rest = rest[pos + 1 :]
                        break
                    else:
                        # Consume any other character.
                        pos += 1

        # Find the next section delimited by `;`, if any.
        if (end := rest.find(";")) == -1:
            break

        rest = rest[end + 1 :].lstrip()

    options: dict[str, str] = {}
    encoding: str | None = None
    continued_encoding: str | None = None

    # For each collected part, process optional charset and continuation,
    # unquote quoted values.
    for pk, pv in parts:
        if pk[-1] == "*":
            # key*=charset''value becomes key=value, where value is percent encoded
            pk = pk[:-1]
            match = _charset_value_re.match(pv)

            if match:
                # If there is a valid charset marker in the value, split it off.
                encoding, pv = match.groups()
                # This might be the empty string, handled next.
                encoding = encoding.lower()

            # No charset marker, or marker with empty charset value.
            if not encoding:
                encoding = continued_encoding

            # A safe list of encodings. Modern clients should only send ASCII or UTF-8.
            # This list will not be extended further. An invalid encoding will leave the
            # value quoted.
            if encoding in {"ascii", "us-ascii", "utf-8", "iso-8859-1"}:
                # Continuation parts don't require their own charset marker. This is
                # looser than the RFC, it will persist across different keys and allows
                # changing the charset during a continuation. But this implementation is
                # much simpler than tracking the full state.
                continued_encoding = encoding
                # invalid bytes are replaced during unquoting
                pv = unquote(pv, encoding=encoding)

        # Remove quotes. At this point the value cannot be empty or a single quote.
        if pv[0] == pv[-1] == '"':
            # HTTP headers use slash, multipart form data uses percent
            pv = pv[1:-1].replace("\\\\", "\\").replace('\\"', '"').replace("%22", '"')

        match = _continuation_re.search(pk)

        if match:
            # key*0=a; key*1=b becomes key=ab
            pk = pk[: match.start()]
            options[pk] = options.get(pk, "") + pv
        else:
            options[pk] = pv

    return value, options

