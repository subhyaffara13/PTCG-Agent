
def utcfromtimestamp(timestamp):
    """Returns the UTC datetime from a timestamp.

    Args:
        timestamp (float): The timestamp to convert.

    Returns:
        datetime: The time in UTC.
    """
    # We used datetime.utcfromtimestamp() before, since it's deprecated from
    # python 3.12, we are using datetime.fromtimestamp(timestamp, timezone.utc)
    # now. "utcfromtimestamp()" is offset-native (no timezone info), but
    # "fromtimestamp(timestamp, timezone.utc)" is offset-aware (with timezone
    # info). This will cause datetime comparison problem. For backward
    # compatibility, we need to remove the timezone info.
    dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    dt = dt.replace(tzinfo=None)
    return dt

