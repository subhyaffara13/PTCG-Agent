import time

def asctime(t=None):
    """
    Convert a tuple or struct_time representing a time as returned by gmtime()
    or localtime() to a 24-character string of the following form:

    >>> asctime(time.gmtime(0))
    'Thu Jan  1 00:00:00 1970'

    If t is not provided, the current time as returned by localtime() is used.
    Locale information is not used by asctime().

    This is meant to normalise the output of the built-in time.asctime() across
    different platforms and Python versions.
    In Python 3.x, the day of the month is right-justified, whereas on Windows
    Python 2.7 it is padded with zeros.

    See https://github.com/fonttools/fonttools/issues/455
    """
    if t is None:
        t = time.localtime()
    s = "%s %s %2s %s" % (
        DAYNAMES[t.tm_wday],
        MONTHNAMES[t.tm_mon],
        t.tm_mday,
        time.strftime("%H:%M:%S %Y", t),
    )
    return s

