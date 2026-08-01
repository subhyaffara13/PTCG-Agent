
def test_dtype_refcount_leak():
    from sys import getrefcount

    dtype = np.dtype(np.float_)
    a = np.array([1], dtype=dtype)
    before = getrefcount(dtype)
    m.ndim(a)
    after = getrefcount(dtype)
    assert after == before

