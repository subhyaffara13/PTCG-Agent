
def test_huge_float(dtype):
    # Covers a non-optimized path that is rarely taken:
    field = "0" * 1000 + ".123456789"
    dtype = np.dtype(dtype)
    value = np.loadtxt([field], dtype=dtype)[()]
    assert value == dtype.type("0.123456789")

