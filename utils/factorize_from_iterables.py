
def factorize_from_iterables(iterables) -> tuple[list[np.ndarray], list[Index]]:
    """
    A higher-level wrapper over `factorize_from_iterable`.

    Parameters
    ----------
    iterables : list-like of list-likes

    Returns
    -------
    codes : list of ndarrays
    categories : list of Indexes

    Notes
    -----
    See `factorize_from_iterable` for more info.
    """
    if len(iterables) == 0:
        # For consistency, it should return two empty lists.
        return [], []

    codes, categories = zip(
        *(factorize_from_iterable(it) for it in iterables),
        strict=True,
    )
    return list(codes), list(categories)

