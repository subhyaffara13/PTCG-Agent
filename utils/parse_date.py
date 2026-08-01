
def parse_date(value: str | None) -> datetime | None:
    """Parse an :rfc:`2822` date into a timezone-aware
    :class:`datetime.datetime` object, or ``None`` if parsing fails.

    This is a wrapper for :func:`email.utils.parsedate_to_datetime`. It
    returns ``None`` if parsing fails instead of raising an exception,
    and always returns a timezone-aware datetime object. If the string
    doesn't have timezone information, it is assumed to be UTC.

    :param value: A string with a supported date format.

    .. versionchanged:: 2.0
        Return a timezone-aware datetime object. Use
        ``email.utils.parsedate_to_datetime``.
    """
    if value is None:
        return None

    try:
        dt = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)

    return dt


def parse_date(value: Union[date, StrBytesIntFloat]) -> date:
    """
    Parse a date/int/float/string and return a datetime.date.

    Raise ValueError if the input is well formatted but not a valid date.
    Raise ValueError if the input isn't well formatted.
    """
    if isinstance(value, date):
        if isinstance(value, datetime):
            return value.date()
        else:
            return value

    number = get_numeric(value, 'date')
    if number is not None:
        return from_unix_seconds(number).date()

    if isinstance(value, bytes):
        value = value.decode()

    match = date_re.match(value)  # type: ignore
    if match is None:
        raise errors.DateError()

    kw = {k: int(v) for k, v in match.groupdict().items()}

    try:
        return date(**kw)
    except ValueError:
        raise errors.DateError()


def parse_date(value: Union[date, StrBytesIntFloat]) -> date:
    return _parse_date(value)


def parse_date(value: Union[date, StrBytesIntFloat]) -> date:
    """
    Parse a date/int/float/string and return a datetime.date.

    Raise ValueError if the input is well formatted but not a valid date.
    Raise ValueError if the input isn't well formatted.
    """
    if isinstance(value, date):
        if isinstance(value, datetime):
            return value.date()
        else:
            return value

    number = _get_numeric(value, "date")
    if number is not None:
        return _from_unix_seconds(number).date()

    if isinstance(value, bytes):
        value = value.decode()

    assert not isinstance(value, (float, int))
    match = date_re.match(value)
    if match is None:
        raise ValueError("invalid date format")

    kw = {k: int(v) for k, v in match.groupdict().items()}

    try:
        return date(**kw)
    except ValueError:
        raise ValueError("invalid date format") from None

