
def test_scalar_extraction():
    """Confirm that extracting a value doesn't convert to python float"""
    o = 1 + LD_INFO.eps
    a = np.array([o, o, o])
    assert_equal(a[1], o)

