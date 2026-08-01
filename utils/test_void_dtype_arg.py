
def test_void_dtype_arg():
    # Basic test for the dtype argument (positional and keyword)
    res = np.void((1, 2), dtype="i,i")
    assert res.item() == (1, 2)
    res = np.void((2, 3), "i,i")
    assert res.item() == (2, 3)

