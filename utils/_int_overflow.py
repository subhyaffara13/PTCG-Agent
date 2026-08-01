
def _int_overflow(x, exception, msg=None):
    """Cast the value to a dfitpack_int and raise an OverflowError if the value
    cannot fit.
    """
    if x > iinfo(dfitpack_int).max:
        if msg is None:
            msg = f'{x!r} cannot fit into an {dfitpack_int!r}'
        raise exception(msg)
    return dfitpack_int(x)

