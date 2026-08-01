
def _arg_wlen_as_expected(value):
    """Ensure argument `wlen` is of type `np.intp` and larger than 1.

    Used in `peak_prominences` and `peak_widths`.

    Returns
    -------
    value : np.intp
        The original `value` rounded up to an integer or -1 if `value` was
        None.
    """
    if value is None:
        # _peak_prominences expects an intp; -1 signals that no value was
        # supplied by the user
        value = -1
    elif 1 < value:
        # Round up to a positive integer
        if isinstance(value, float):
            value = math.ceil(value)
        value = np.intp(value)
    else:
        raise ValueError(f'`wlen` must be larger than 1, was {value}')
    return value

