import os
import sys

def set_timezone(tz: str) -> Generator[None]:
    """
    Context manager for temporarily setting a timezone.

    Parameters
    ----------
    tz : str
        A string representing a valid timezone.

    Examples
    --------
    >>> from datetime import datetime
    >>> from dateutil.tz import tzlocal
    >>> tzlocal().tzname(datetime(2021, 1, 1))  # doctest: +SKIP
    'IST'

    >>> with set_timezone("US/Eastern"):
    ...     tzlocal().tzname(datetime(2021, 1, 1))
    'EST'
    """
    import time

    def setTZ(tz) -> None:
        if hasattr(time, "tzset"):
            if tz is None:
                try:
                    del os.environ["TZ"]
                except KeyError:
                    pass
            else:
                os.environ["TZ"] = tz
                # Next line allows typing checks to pass on Windows
                if sys.platform != "win32":
                    time.tzset()

    orig_tz = os.environ.get("TZ")
    setTZ(tz)
    try:
        yield
    finally:
        setTZ(orig_tz)

