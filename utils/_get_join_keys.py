
def _get_join_keys(
    llab: list[npt.NDArray[np.int64 | np.intp]],
    rlab: list[npt.NDArray[np.int64 | np.intp]],
    shape: Shape,
    sort: bool,
) -> tuple[npt.NDArray[np.int64], npt.NDArray[np.int64]]:
    # how many levels can be done without overflow
    nlev = next(
        lev
        for lev in range(len(shape), 0, -1)
        if not is_int64_overflow_possible(shape[:lev])
    )

    # get keys for the first `nlev` levels
    stride = np.prod(shape[1:nlev], dtype="i8")
    lkey = stride * llab[0].astype("i8", subok=False, copy=False)
    rkey = stride * rlab[0].astype("i8", subok=False, copy=False)

    for i in range(1, nlev):
        with np.errstate(divide="ignore"):
            stride //= shape[i]
        lkey += llab[i] * stride
        rkey += rlab[i] * stride

    if nlev == len(shape):  # all done!
        return lkey, rkey

    # densify current keys to avoid overflow
    lkey, rkey, count = _factorize_keys(lkey, rkey, sort=sort)

    llab = [lkey, *llab[nlev:]]
    rlab = [rkey, *rlab[nlev:]]
    shape = (count, *shape[nlev:])

    return _get_join_keys(llab, rlab, shape, sort)

