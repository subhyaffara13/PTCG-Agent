
def test_non_standard_params(func, xp):
    # use __name__ so that `lazy_xp_function` doesn't break things
    if func.__name__ in ["rfft", "rfftn", "ihfft"]:
        dtype = xp.float64
    else:
        dtype = xp.complex128

    x = xp.asarray([1, 2, 3], dtype=dtype)
    # func(x) should not raise an exception
    func(x)

    if is_numpy(xp):
        func(x, workers=2)
    else:
        assert_raises(ValueError, func, x, workers=2)

