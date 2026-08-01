
def should_cache(
    arg: ArrayConvertible, unique_share: float = 0.7, check_count: int | None = None
) -> bool:
    """
    Decides whether to do caching.

    If the percent of unique elements among `check_count` elements less
    than `unique_share * 100` then we can do caching.

    Parameters
    ----------
    arg: listlike, tuple, 1-d array, Series
    unique_share: float, default=0.7, optional
        0 < unique_share < 1
    check_count: int, optional
        0 <= check_count <= len(arg)

    Returns
    -------
    do_caching: bool

    Notes
    -----
    By default for a sequence of less than 50 items in size, we don't do
    caching; for the number of elements less than 5000, we take ten percent of
    all elements to check for a uniqueness share; if the sequence size is more
    than 5000, then we check only the first 500 elements.
    All constants were chosen empirically by.
    """
    do_caching = True

    # default realization
    if check_count is None:
        # in this case, the gain from caching is negligible
        if len(arg) <= start_caching_at:
            return False

        if len(arg) <= 5000:
            check_count = len(arg) // 10
        else:
            check_count = 500
    else:
        assert 0 <= check_count <= len(arg), (
            "check_count must be in next bounds: [0; len(arg)]"
        )
        if check_count == 0:
            return False

    assert 0 < unique_share < 1, "unique_share must be in next bounds: (0; 1)"

    try:
        # We can't cache if the items are not hashable.
        unique_elements = set(islice(arg, check_count))
    except TypeError:
        return False
    if len(unique_elements) > check_count * unique_share:
        do_caching = False
    return do_caching

