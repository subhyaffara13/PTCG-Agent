
def test_numpy_ufuncs_other(index, func):
    # test ufuncs of numpy, see:
    # https://numpy.org/doc/stable/reference/ufuncs.html
    if isinstance(index, (DatetimeIndex, TimedeltaIndex)):
        if func in (np.isfinite, np.isinf, np.isnan):
            # numpy 1.18 changed isinf and isnan to not raise on dt64/td64
            result = func(index)

            out = np.empty(index.shape, dtype=bool)
            func(index, out=out)
            tm.assert_index_equal(Index(out), result)
        else:
            with tm.external_error_raised(TypeError):
                func(index)

    elif isinstance(index, PeriodIndex):
        with tm.external_error_raised(TypeError):
            func(index)

    elif is_numeric_dtype(index) and not (
        is_complex_dtype(index) and func is np.signbit
    ):
        # Results in bool array
        result = func(index)
        assert isinstance(result, Index)
        if not isinstance(index.dtype, np.dtype):
            # e.g. Int64 we expect to get BooleanArray back
            assert isinstance(result.dtype, BooleanDtype)
        else:
            assert isinstance(result.dtype, np.dtype)

        out = np.empty(index.shape, dtype=bool)
        func(index, out=out)

        if not isinstance(index.dtype, np.dtype):
            tm.assert_index_equal(result, Index(out, dtype="boolean"))
        else:
            tm.assert_index_equal(result, Index(out))

    elif len(index) == 0:
        pass
    else:
        with tm.external_error_raised(TypeError):
            func(index)

