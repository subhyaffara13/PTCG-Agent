
def parse_accept_header(value: str | None) -> ds.Accept: ...


def parse_accept_header(value: str | None, cls: type[_TAnyAccept]) -> _TAnyAccept: ...


def parse_accept_header(
    value: str | None, cls: type[_TAnyAccept] | None = None
) -> _TAnyAccept:
    """Parse an ``Accept`` header according to
    `RFC 9110 <https://httpwg.org/specs/rfc9110.html#field.accept>`__.

    Returns an :class:`.Accept` instance, which can sort and inspect items based on
    their quality parameter. When parsing ``Accept-Charset``, ``Accept-Encoding``, or
    ``Accept-Language``, pass the appropriate :class:`.Accept` subclass.

    :param value: The header value to parse.
    :param cls: The :class:`.Accept` class to wrap the result in.
    :return: An instance of ``cls``.

    .. versionchanged:: 2.3
        Parse according to RFC 9110. Items with invalid ``q`` values are skipped.
    """
    if cls is None:
        cls = t.cast(type[_TAnyAccept], ds.Accept)

    if not value:
        return cls(None)

    result = []

    for item in parse_list_header(value):
        item, options = parse_options_header(item)

        if "q" in options:
            # pop q, remaining options are reconstructed
            q_str = options.pop("q").strip()

            if _q_value_re.fullmatch(q_str) is None:
                # ignore an invalid q
                continue

            q = float(q_str)

            if q < 0 or q > 1:
                # ignore an invalid q
                continue
        else:
            q = 1

        if options:
            # reconstruct the media type with any options
            item = dump_options_header(item, options)

        result.append((item, q))

    return cls(result)

