
def test___array___refcount():
    class MyArray:
        def __init__(self, dtype):
            self.val = np.array(-1, dtype=dtype)

        def __array__(self, dtype=None, copy=None):
            return self.val.__array__(dtype=dtype, copy=copy)

    # test all possible scenarios:
    # dtype(none | same | different) x copy(true | false | none)
    dt = np.dtype(np.int32)
    old_refcount = sys.getrefcount(dt)
    np.array(MyArray(dt))
    assert_equal(old_refcount, sys.getrefcount(dt))
    np.array(MyArray(dt), dtype=dt)
    assert_equal(old_refcount, sys.getrefcount(dt))
    np.array(MyArray(dt), copy=None)
    assert_equal(old_refcount, sys.getrefcount(dt))
    np.array(MyArray(dt), dtype=dt, copy=None)
    assert_equal(old_refcount, sys.getrefcount(dt))
    dt2 = np.dtype(np.int16)
    old_refcount2 = sys.getrefcount(dt2)
    np.array(MyArray(dt), dtype=dt2)
    assert_equal(old_refcount2, sys.getrefcount(dt2))
    np.array(MyArray(dt), dtype=dt2, copy=None)
    assert_equal(old_refcount2, sys.getrefcount(dt2))
    with pytest.raises(ValueError):
        np.array(MyArray(dt), dtype=dt2, copy=False)
    assert_equal(old_refcount2, sys.getrefcount(dt2))

