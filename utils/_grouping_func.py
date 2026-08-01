
def _grouping_func(tup: tuple[int, ArrayLike]) -> tuple[int, DtypeObj]:
    dtype = tup[1].dtype

    if is_1d_only_ea_dtype(dtype):
        # We know these won't be consolidated, so don't need to group these.
        # This avoids expensive comparisons of CategoricalDtype objects
        sep = id(dtype)
    else:
        sep = 0

    return sep, dtype

