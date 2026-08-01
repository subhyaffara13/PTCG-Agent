
def test_str_roundtrip_bytes():
    o = 1 + LD_INFO.eps
    assert_equal(np.longdouble(str(o).encode("ascii")), o)

