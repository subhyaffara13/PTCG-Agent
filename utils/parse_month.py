
def parse_month(raw_month: str) -> int:
    """Convert ``str`` to a month (``int``).

    >>> parse_month('July')
    7
    >>> parse_month('december')
    12

    :param raw_month: The raw month.
    :return: The converted month.
    """
    return datetime.strptime(raw_month, '%B').month

