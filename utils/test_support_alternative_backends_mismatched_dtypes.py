
def test_support_alternative_backends_mismatched_dtypes(xp, func, nfo):
    """Test mix-n-match of int and float arguments"""
    if func.__name__ in {'expn', 'polygamma', 'multigammaln', 'bdtr', 'bdtrc', 'bdtri',
                         'nbdtr', 'nbdtrc', 'nbdtri', 'pdtri'}:
        pytest.skip(f"dtypes for {func.__name__} make it a bad fit for this test.")
    dtypes = ['intp', 'float32', 'float64', 'float64'][:nfo.n_args]

    positive_only, dtypes = _skip_or_tweak_alternative_backends(
        xp, nfo, dtypes, (False,)*nfo.n_args
    )
    dtypes_np = [getattr(np, dtype) for dtype in dtypes]
    dtypes_xp = [getattr(xp, dtype) for dtype in dtypes]

    rng = np.random.default_rng(984254252920492019)
    iinfo = np.iinfo(np.intp)
    if nfo.test_large_ints:
        randint = partial(rng.integers, iinfo.min, iinfo.max + 1)
    else:
        randint = partial(rng.integers, -20, 21)
    args_np = [
        randint(size=1, dtype=np.int64),
        rng.standard_normal(size=1, dtype=np.float32),
        rng.standard_normal(size=1, dtype=np.float64),
        rng.standard_normal(size=1, dtype=np.float64),
    ][:nfo.n_args]
    args_np = [
        np.abs(arg) if cond else arg for arg, cond in zip(args_np, positive_only)
    ]

    args_xp = [xp.asarray(arg, dtype=dtype_xp)
               for arg, dtype_xp in zip(args_np, dtypes_xp)]
    args_np = [np.asarray(arg, dtype=dtype_np)
               for arg, dtype_np in zip(args_np, dtypes_np)]

    res = nfo.wrapper(*args_xp)  # Also wrapped by lazy_xp_function
    ref = nfo.func(*args_np)  # Unwrapped ufunc
    if (
            is_torch(xp)
            and xpx.default_dtype(xp) == xp.float32
            and "float64" not in dtypes
    ):
        # int64 promotes like float32 on torch with default dtype = float32
        # cast reference if needed
        ref = np.float32(ref)

    atol = 10 * np.finfo(ref.dtype).eps
    xp_assert_close(res, xp.asarray(ref), atol=atol)

