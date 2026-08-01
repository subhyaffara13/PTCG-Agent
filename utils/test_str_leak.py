
def test_str_leak():
    from sys import getrefcount

    fmt = "f4"
    pytest.gc_collect()
    start = getrefcount(fmt)
    d = m.dtype_wrapper(fmt)
    assert d is np.dtype("f4")
    del d
    pytest.gc_collect()
    assert getrefcount(fmt) == start

