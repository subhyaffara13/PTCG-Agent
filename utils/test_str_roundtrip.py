
def test_str_roundtrip():
    # We will only see eps in repr if within printing precision.
    o = 1 + LD_INFO.eps
    assert_equal(np.longdouble(str(o)), o, f"str was {str(o)}")

