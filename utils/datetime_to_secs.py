
def datetime_to_secs(value):
    """Convert a datetime object to the number of seconds since the UNIX epoch.

    Args:
        value (datetime): The datetime to convert.

    Returns:
        int: The number of seconds since the UNIX epoch.
    """
    return calendar.timegm(value.utctimetuple())

