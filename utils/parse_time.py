import time
from typing import Dict, Union

def parse_time(raw_time: str) -> time:
    """Convert ``str`` to a ``datetime.time``.

    >>> parse_time('12:34:56')
    datetime.time(12, 34, 56)

    :param raw_time: The raw time.
    :return: The converted time.
    """
    return datetime.strptime(raw_time, '%H:%M:%S').time()


def parse_time(value: Union[time, StrBytesIntFloat]) -> time:
    """
    Parse a time/string and return a datetime.time.

    Raise ValueError if the input is well formatted but not a valid time.
    Raise ValueError if the input isn't well formatted, in particular if it contains an offset.
    """
    if isinstance(value, time):
        return value

    number = get_numeric(value, 'time')
    if number is not None:
        if number >= 86400:
            # doesn't make sense since the time time loop back around to 0
            raise errors.TimeError()
        return (datetime.min + timedelta(seconds=number)).time()

    if isinstance(value, bytes):
        value = value.decode()

    match = time_re.match(value)  # type: ignore
    if match is None:
        raise errors.TimeError()

    kw = match.groupdict()
    if kw['microsecond']:
        kw['microsecond'] = kw['microsecond'].ljust(6, '0')

    tzinfo = _parse_timezone(kw.pop('tzinfo'), errors.TimeError)
    kw_: Dict[str, Union[None, int, timezone]] = {k: int(v) for k, v in kw.items() if v is not None}
    kw_['tzinfo'] = tzinfo

    try:
        return time(**kw_)  # type: ignore
    except ValueError:
        raise errors.TimeError()

