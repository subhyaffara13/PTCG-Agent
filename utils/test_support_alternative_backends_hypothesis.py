
def test_support_alternative_backends_hypothesis(xp, func, nfo, data):
    if func.__name__ in {'expn', 'polygamma', 'multigammaln', 'bdtr', 'bdtrc', 'bdtri',
                         'nbdtr', 'nbdtrc', 'nbdtri', 'pdtri'}:
        pytest.skip(f"dtypes for {func.__name__} make it a bad fit for this test.")
    dtype = data.draw(strategies.sampled_from(['float32', 'float64', 'intp']))
    positive_only, dtypes = _skip_or_tweak_alternative_backends(
        xp, nfo, [dtype], (False,)*nfo.n_args
    )
    dtype_np = getattr(np, dtypes[0])
    dtype_xp = getattr(xp, dtypes[0])

    elements = {'allow_subnormal': False}
    # Most failures are due to NaN or infinity; uncomment to suppress them
    # elements['allow_infinity'] = False
    # elements['allow_nan'] = False
    if any(positive_only):
        elements['min_value'] = 0

    shapes, _ = data.draw(
        npst.mutually_broadcastable_shapes(num_shapes=nfo.n_args))
    args_np = [data.draw(npst.arrays(dtype_np, shape, elements=elements))
               for shape in shapes]

    args_xp = [xp.asarray(arg, dtype=dtype_xp) for arg in args_np]
    args_np = [np.asarray(arg, dtype=dtype_np) for arg in args_np]

    res = nfo.wrapper(*args_xp)  # Also wrapped by lazy_xp_function
    ref = nfo.func(*args_np)  # Unwrapped ufunc
    if (
            is_torch(xp)
            and xpx.default_dtype(xp) == xp.float32
            and dtype != "float64"
    ):
        # int64 promotes like float32 on torch with default dtype = float32
        # cast reference if needed
        ref = np.float32(ref)

    # When dtype_np is integer, the output dtype can be float
    atol = 0 if ref.dtype.kind in 'iu' else 10 * np.finfo(ref.dtype).eps
    xp_assert_close(res, xp.asarray(ref), atol=atol)

