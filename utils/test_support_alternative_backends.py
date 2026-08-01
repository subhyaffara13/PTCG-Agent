
def test_support_alternative_backends(xp, func, nfo, base_dtype, shapes):
    int_only = nfo.int_only
    if int_only is None:
        int_only = (False, ) * nfo.n_args
        dtypes = (base_dtype, ) * nfo.n_args
    else:
        dtypes = tuple(
            'intp' if needs_int else base_dtype for needs_int in int_only
        )

    positive_only, dtypes = _skip_or_tweak_alternative_backends(
        xp, nfo, dtypes, int_only
    )

    dtypes_np = [getattr(np, dtype) for dtype in dtypes]
    dtypes_xp = [getattr(xp, dtype) for dtype in dtypes]

    shapes = shapes[:nfo.n_args]
    rng = np.random.default_rng(984254252920492019)
    args_np = []

    # Handle cases where there's an argument which only takes scalar values.
    python_int_only = nfo.python_int_only
    if isinstance(python_int_only, dict):
        python_int_only = python_int_only.get(get_native_namespace_name(xp))
    scalar_or_0d_only = nfo.scalar_or_0d_only
    if isinstance(scalar_or_0d_only, dict):
        scalar_or_0d_only = scalar_or_0d_only.get(get_native_namespace_name(xp))

    test_large_ints = nfo.test_large_ints
    if isinstance(nfo.test_large_ints, dict):
        test_large_ints = test_large_ints.get(get_native_namespace_name(xp), False)

    if python_int_only is None:
        python_int_only = [False] * nfo.n_args
    if scalar_or_0d_only is None:
        scalar_or_0d_only = [False] * nfo.n_args

    no_shape = [
        cond1 or cond2 for cond1, cond2 in zip(python_int_only, scalar_or_0d_only)
    ]

    shapes = [shape if not cond else None for shape, cond in zip(shapes, no_shape)]

    for dtype, dtype_np, shape, needs_python_int in zip(
            dtypes, dtypes_np, shapes, python_int_only
    ):
        if 'int' in dtype and test_large_ints:
            iinfo = np.iinfo(dtype_np)
            rand = partial(rng.integers, iinfo.min, iinfo.max + 1)
        elif 'int' in dtype:
            rand = partial(rng.integers, -20, 21)
        else:
            rand = rng.standard_normal
        val = rand(size=shape, dtype=dtype_np)
        if needs_python_int:
            # The logic above for determining shapes guarantees that
            # shape will be None in the above line when a Python int is required,
            # so this can safely be converted to an int.
            val = int(val)
        args_np.append(val)

    args_np = [
        np.abs(arg) if cond else arg for arg, cond in zip(args_np, positive_only)
    ]

    args_xp = [
        xp.asarray(arg, dtype=dtype_xp) if not needs_python_int
        else arg
        for arg, dtype_xp, needs_python_int
        in zip(args_np, dtypes_xp, python_int_only)
    ]

    args_np = [
        np.asarray(arg, dtype=dtype_np) if not needs_python_int
        else arg
        for arg, dtype_np, needs_python_int
        in zip(args_np, dtypes_np, python_int_only)
    ]

    if is_dask(xp):
        # We're using map_blocks to dispatch the function to Dask.
        # This is the correct thing to do IF all tested functions are elementwise;
        # otherwise the output would change depending on chunking.
        # Try to trigger bugs related to having multiple chunks.
        args_xp = [arg.rechunk(5) for arg in args_xp]

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
    # When dtype_np is integer, the output dtype can be float
    atol = 0 if ref.dtype.kind in 'iu' else 10 * np.finfo(ref.dtype).eps
    rtol = None
    if is_torch(xp) and func.__name__ == 'j1':
        # If we end up needing more function/backend specific tolerance
        # adjustments, this should be factored out properly.
        atol = 1e-7
        rtol = 1e-5
    xp_assert_close(
        res, xp.asarray(ref), rtol=rtol, atol=atol, check_0d=nfo.produces_0d
    )

