
def parse_datetime(value: Union[datetime, StrBytesIntFloat]) -> datetime:
    """
    Parse a datetime/int/float/string and return a datetime.datetime.

    This function supports time zone offsets. When the input contains one,
    the output uses a timezone with a fixed offset from UTC.

    Raise ValueError if the input is well formatted but not a valid datetime.
    Raise ValueError if the input isn't well formatted.
    """
    if isinstance(value, datetime):
        return value

    number = get_numeric(value, 'datetime')
    if number is not None:
        return from_unix_seconds(number)

    if isinstance(value, bytes):
        value = value.decode()

    match = datetime_re.match(value)  # type: ignore
    if match is None:
        raise errors.DateTimeError()

    kw = match.groupdict()
    if kw['microsecond']:
        kw['microsecond'] = kw['microsecond'].ljust(6, '0')

    tzinfo = _parse_timezone(kw.pop('tzinfo'), errors.DateTimeError)
    kw_: Dict[str, Union[None, int, timezone]] = {k: int(v) for k, v in kw.items() if v is not None}
    kw_['tzinfo'] = tzinfo

    try:
        return datetime(**kw_)  # type: ignore
    except ValueError:
        raise errors.DateTimeError()


def parse_datetime(value: Union[datetime, StrBytesIntFloat]) -> datetime:
    return _parse_datetime(value)


def parse_datetime(value: Union[datetime, StrBytesIntFloat]) -> datetime:
    """
    Parse a datetime/int/float/string and return a datetime.datetime.

    This function supports time zone offsets. When the input contains one,
    the output uses a timezone with a fixed offset from UTC.

    Raise ValueError if the input is well formatted but not a valid datetime.
    Raise ValueError if the input isn't well formatted.
    """
    if isinstance(value, datetime):
        return value

    number = _get_numeric(value, "datetime")
    if number is not None:
        return _from_unix_seconds(number)

    if isinstance(value, bytes):
        value = value.decode()

    assert not isinstance(value, (float, int))

    match = datetime_re.match(value)
    if match is None:
        raise ValueError("invalid datetime format")

    kw = match.groupdict()
    if kw["microsecond"]:
        kw["microsecond"] = kw["microsecond"].ljust(6, "0")

    tzinfo = _parse_timezone(kw.pop("tzinfo"))
    kw_: Dict[str, Union[None, int, timezone]] = {k: int(v) for k, v in kw.items() if v is not None}
    kw_["tzinfo"] = tzinfo

    return datetime(**kw_)  # type: ignore


def parse_datetime(date_string: str) -> datetime:
    """
    Parses a date_string returned from the server to a datetime object.

    This parser is a weak-parser is the sense that it handles only a single format of
    date_string. It is expected that the server format will never change. The
    implementation depends only on the standard lib to avoid an external dependency
    (python-dateutil). See full discussion about this decision on PR:
    https://github.com/huggingface/huggingface_hub/pull/999.

    Example:
        ```py
        > parse_datetime('2022-08-19T07:19:38.123Z')
        datetime.datetime(2022, 8, 19, 7, 19, 38, 123000, tzinfo=timezone.utc)
        ```

    Args:
        date_string (`str`):
            A string representing a datetime returned by the Hub server.
            String is expected to follow '%Y-%m-%dT%H:%M:%S.%fZ' pattern.

    Returns:
        A python datetime object.

    Raises:
        :class:`ValueError`:
            If `date_string` cannot be parsed.
    """
    try:
        # Normalize the string to always have 6 digits of fractional seconds
        if date_string.endswith("Z"):
            # Case 1: No decimal point (e.g., "2024-11-16T00:27:02Z")
            if "." not in date_string:
                # No fractional seconds - insert .000000
                date_string = date_string[:-1] + ".000000Z"
            # Case 2: Has decimal point (e.g., "2022-08-19T07:19:38.123456789Z")
            else:
                # Get the fractional and base parts
                base, fraction = date_string[:-1].split(".")
                # fraction[:6] takes first 6 digits and :0<6 pads with zeros if less than 6 digits
                date_string = f"{base}.{fraction[:6]:0<6}Z"

        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
    except ValueError as e:
        raise ValueError(
            f"Cannot parse '{date_string}' as a datetime. Date string is expected to"
            " follow '%Y-%m-%dT%H:%M:%S.%fZ' pattern."
        ) from e

