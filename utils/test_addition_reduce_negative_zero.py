
def test_addition_reduce_negative_zero(dtype, use_initial):
    dtype = np.dtype(dtype)
    if dtype.kind == "c":
        neg_zero = dtype.type(complex(-0.0, -0.0))
    else:
        neg_zero = dtype.type(-0.0)

    kwargs = {}
    if use_initial:
        kwargs["initial"] = neg_zero
    else:
        pytest.xfail("-0. propagation in sum currently requires initial")

    # Test various length, in case SIMD paths or chunking play a role.
    # 150 extends beyond the pairwise blocksize; probably not important.
    for i in range(150):
        arr = np.array([neg_zero] * i, dtype=dtype)
        res = np.sum(arr, **kwargs)
        if i > 0 or use_initial:
            assert _check_neg_zero(res)
        else:
            # `sum([])` should probably be 0.0 and not -0.0 like `sum([-0.0])`
            assert not np.signbit(res.real)
            assert not np.signbit(res.imag)

