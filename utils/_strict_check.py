
def _strict_check(actual, desired, xp, *,
                  check_namespace=True, check_dtype=True, check_shape=True,
                  check_0d=True):
    __tracebackhide__ = True  # Hide traceback for py.test

    if xp is None:
        try:
            xp = _default_xp_ctxvar.get()
        except LookupError:
            xp = array_namespace(desired)

    if check_namespace:
        _assert_matching_namespace(actual, desired, xp)

    # only NumPy distinguishes between scalars and arrays; we do if check_0d=True.
    # do this first so we can then cast to array (and thus use the array API) below.
    if is_numpy(xp) and check_0d:
        _msg = ("Array-ness does not match:\n Actual: "
                f"{type(actual)}\n Desired: {type(desired)}")
        assert ((xp.isscalar(actual) and xp.isscalar(desired))
                or (not xp.isscalar(actual) and not xp.isscalar(desired))), _msg

    actual = xp.asarray(actual)
    desired = xp.asarray(desired)

    if check_dtype:
        _msg = f"dtypes do not match.\nActual: {actual.dtype}\nDesired: {desired.dtype}"
        assert actual.dtype == desired.dtype, _msg

    if check_shape:
        if is_dask(xp):
            actual.compute_chunk_sizes()
            desired.compute_chunk_sizes()
        _msg = f"Shapes do not match.\nActual: {actual.shape}\nDesired: {desired.shape}"
        assert actual.shape == desired.shape, _msg

    desired = xp.broadcast_to(desired, actual.shape)
    return actual, desired, xp

