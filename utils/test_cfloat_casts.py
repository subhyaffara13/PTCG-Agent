
def test_cfloat_casts(typename):
    inp = [1.1 + 1.1j, 2.8 + 2.8j, -3.2 - 3.2j, 2.7e4 + 2.7e4j]
    ainp = np.array(inp, dtype=typename)
    assert_array_equal(ainp, ainp.astype("T").astype(typename))

    inp = [0.1 + 0.1j]
    sres = np.array(inp, dtype=typename).astype("T")
    res = sres.astype(typename)
    assert_array_equal(np.array(inp, dtype=typename), res)
    assert sres[0] == "(0.1+0.1j)"

