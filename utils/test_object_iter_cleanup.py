
def test_object_iter_cleanup():
    # see gh-18450
    # object arrays can raise a python exception in ufunc inner loops using
    # nditer, which should cause iteration to stop & cleanup. There were bugs
    # in the nditer cleanup when decref'ing object arrays.
    # This test would trigger valgrind "uninitialized read" before the bugfix.
    assert_raises(TypeError, lambda: np.zeros((17000, 2), dtype='f4') * None)

    # this more explicit code also triggers the invalid access
    arr = np.arange(ncu.BUFSIZE * 10).reshape(10, -1).astype(str)
    oarr = arr.astype(object)
    oarr[:, -1] = None
    assert_raises(TypeError, lambda: np.add(oarr[:, ::-1], arr[:, ::-1]))

    # followup: this tests for a bug introduced in the first pass of gh-18450,
    # caused by an incorrect fallthrough of the TypeError
    class T:
        def __bool__(self):
            raise TypeError("Ambiguous")
    assert_raises(TypeError, np.logical_or.reduce,
                             np.array([T(), T()], dtype='O'))

