
def utcnow():
    """Returns the current UTC datetime.

    Returns:
        datetime: The current time in UTC.
    """
    # We used datetime.utcnow() before, since it's deprecated from python 3.12,
    # we are using datetime.now(timezone.utc) now. "utcnow()" is offset-native
    # (no timezone info), but "now()" is offset-aware (with timezone info).
    # This will cause datetime comparison problem. For backward compatibility,
    # we need to remove the timezone info.
    now = datetime.datetime.now(datetime.timezone.utc)
    now = now.replace(tzinfo=None)
    return now

