
def isna_all(arr: ArrayLike) -> bool:
    """
    Optimized equivalent to isna(arr).all()
    """
    total_len = len(arr)

    # Usually it's enough to check but a small fraction of values to see if
    #  a block is NOT null, chunks should help in such cases.
    #  parameters 1000 and 40 were chosen arbitrarily
    chunk_len = max(total_len // 40, 1000)

    dtype = arr.dtype
    if lib.is_np_dtype(dtype, "f"):
        checker = np.isnan

    elif (lib.is_np_dtype(dtype, "mM")) or isinstance(
        dtype, (DatetimeTZDtype, PeriodDtype)
    ):
        # error: Incompatible types in assignment (expression has type
        # "Callable[[Any], Any]", variable has type "ufunc")
        checker = lambda x: np.asarray(x.view("i8")) == iNaT  # type: ignore[assignment]

    else:
        # error: Incompatible types in assignment (expression has type "Callable[[Any],
        # Any]", variable has type "ufunc")
        checker = _isna_array  # type: ignore[assignment]

    return all(
        checker(arr[i : i + chunk_len]).all() for i in range(0, total_len, chunk_len)
    )

