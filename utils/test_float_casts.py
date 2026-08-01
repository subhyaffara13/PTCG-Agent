
def test_float_casts(typename):
    inp = [1.1, 2.8, -3.2, 2.7e4]
    ainp = np.array(inp, dtype=typename)
    assert_array_equal(ainp, ainp.astype("T").astype(typename))

    inp = [0.1]
    sres = np.array(inp, dtype=typename).astype("T")
    res = sres.astype(typename)
    assert_array_equal(np.array(inp, dtype=typename), res)
    assert sres[0] == "0.1"

    if typename == "longdouble":
        # let's not worry about platform-dependent rounding of longdouble
        return

    fi = np.finfo(typename)

    inp = [1e-324, fi.smallest_subnormal, -1e-324, -fi.smallest_subnormal]
    eres = [0, fi.smallest_subnormal, -0, -fi.smallest_subnormal]
    res = np.array(inp, dtype=typename).astype("T").astype(typename)
    assert_array_equal(eres, res)

    inp = [2e308, fi.max, -2e308, fi.min]
    eres = [np.inf, fi.max, -np.inf, fi.min]
    res = np.array(inp, dtype=typename).astype("T").astype(typename)
    assert_array_equal(eres, res)

