
def test_ufunc_kwargs(func, n_args, int_only, is_ufunc):
    """Test that numpy-specific out= and dtype= keyword arguments
    of ufuncs still work when SCIPY_ARRAY_API is set.
    """
    if not is_ufunc:
        pytest.skip(f"{func.__name__} is not a ufunc.")
    if int_only is None:
        int_only = (False, ) * n_args
    # out=
    args = [
        np.asarray([.1, .2]) if not needs_int
        else np.asarray([1, 2])
        for needs_int in int_only
    ]
    out = np.empty(2)
    y = func(*args, out=out)
    xp_assert_close(y, out)

    # out= with out.dtype != args.dtype
    out = np.empty(2, dtype=np.float32)
    y = func(*args, out=out)
    xp_assert_close(y, out)

    if func.__name__ in {"bdtr", "bdtrc", "bdtri"}:
        # The below function evaluation will trigger a deprecation warning
        # with dtype=np.float32. This will go away if the trigger is actually
        # pulled on the deprecation.
        return

    # dtype=
    y = func(*args, dtype=np.float32)
    assert y.dtype == np.float32

