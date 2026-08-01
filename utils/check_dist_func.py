
def check_dist_func(dist, fname, arg, result_shape, methods):
    # Check that all computation methods of all distribution functions agree
    # with one another, effectively testing the correctness of the generic
    # computation methods and confirming the consistency of specific
    # distributions with their pdf/logpdf.

    args = tuple() if arg is None else (arg,)
    methods = methods.copy()

    if "cache" in methods:
        # If "cache" is specified before the value has been evaluated, it
        # raises an error. After the value is evaluated, it will succeed.
        with pytest.raises(NotImplementedError):
            getattr(dist, fname)(*args, method="cache")

    ref = getattr(dist, fname)(*args)
    check_nans_and_edges(dist, fname, arg, ref)

    # Remove this after fixing `draw`
    tol_override = {'atol': 1e-15}
    # Mean can be 0, which makes logmean -inf.
    if fname in {'logmean', 'mean', 'logskewness', 'skewness'}:
        tol_override = {'atol': 1e-15}
    elif fname in {'mode'}:
        # can only expect about half of machine precision for optimization
        # because math
        tol_override = {'atol': 1e-6}
    elif fname in {'logcdf'}:  # gh-22276
        tol_override = {'rtol': 2e-7}

    if dist._overrides(f'_{fname}_formula'):
        methods.add('formula')

    np.testing.assert_equal(ref.shape, result_shape)
    # Until we convert to array API, let's do the familiar thing:
    # 0d things are scalars, not arrays
    if result_shape == tuple():
        assert np.isscalar(ref)

    for method in methods:
        res = getattr(dist, fname)(*args, method=method)
        if 'log' in fname:
            np.testing.assert_allclose(np.exp(res), np.exp(ref),
                                       **tol_override)
        else:
            np.testing.assert_allclose(res, ref, **tol_override)

        # for now, make sure dtypes are consistent; later, we can check whether
        # they are correct.
        np.testing.assert_equal(res.dtype, ref.dtype)
        np.testing.assert_equal(res.shape, result_shape)
        if result_shape == tuple():
            assert np.isscalar(res)

