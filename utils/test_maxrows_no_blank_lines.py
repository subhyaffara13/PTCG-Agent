
def test_maxrows_no_blank_lines(dtype):
    txt = StringIO("1.5,2.5\n3.0,4.0\n5.5,6.0")
    res = np.loadtxt(txt, dtype=dtype, delimiter=",", max_rows=2)
    assert_equal(res.dtype, dtype)
    assert_equal(res, np.array([["1.5", "2.5"], ["3.0", "4.0"]], dtype=dtype))

