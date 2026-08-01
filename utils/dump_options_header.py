
def dump_options_header(header: str | None, options: t.Mapping[str, t.Any]) -> str:
    """Produce a header value and ``key=value`` parameters separated by semicolons
    ``;``. For example, the ``Content-Type`` header.

    .. code-block:: python

        dump_options_header("text/html", {"charset": "UTF-8"})
        'text/html; charset=UTF-8'

    This is the reverse of :func:`parse_options_header`.

    If a value contains non-token characters, it will be quoted.

    If a value is ``None``, the parameter is skipped.

    In some keys for some headers, a UTF-8 value can be encoded using a special
    ``key*=UTF-8''value`` form, where ``value`` is percent encoded. This function will
    not produce that format automatically, but if a given key ends with an asterisk
    ``*``, the value is assumed to have that form and will not be quoted further.

    :param header: The primary header value.
    :param options: Parameters to encode as ``key=value`` pairs.

    .. versionchanged:: 2.3
        Keys with ``None`` values are skipped rather than treated as a bare key.

    .. versionchanged:: 2.2.3
        If a key ends with ``*``, its value will not be quoted.
    """
    segments = []

    if header is not None:
        segments.append(header)

    for key, value in options.items():
        if value is None:
            continue

        if key[-1] == "*":
            segments.append(f"{key}={value}")
        else:
            segments.append(f"{key}={quote_header_value(value)}")

    return "; ".join(segments)

