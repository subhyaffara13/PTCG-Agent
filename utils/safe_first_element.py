
def safe_first_element(obj):
    """
    Return the first element in *obj*.

    This is a type-independent way of obtaining the first element,
    supporting both index access and the iterator protocol.
    """
    if isinstance(obj, collections.abc.Iterator):
        # needed to accept `array.flat` as input.
        # np.flatiter reports as an instance of collections.Iterator but can still be
        # indexed via []. This has the side effect of re-setting the iterator, but
        # that is acceptable.
        try:
            return obj[0]
        except TypeError:
            pass
        raise RuntimeError("matplotlib does not support generators as input")
    return next(iter(obj))

