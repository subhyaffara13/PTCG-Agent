
def _secs2timedelta(secs):
    """
    Convert seconds to hh:mm:ss.msec, msecs rounded to 2 decimal places.
    """

    msec = int(abs(secs - int(secs)) * 100)
    return f"{datetime.timedelta(seconds=int(secs))}.{msec:02d}"

