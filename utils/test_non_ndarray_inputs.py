
def test_non_ndarray_inputs():
    # Regression check for gh-5604

    class MyArray:
        def __init__(self, data):
            self.data = data

        @property
        def __array_interface__(self):
            return self.data.__array_interface__

    class MyArray2:
        def __init__(self, data):
            self.data = data

        def __array__(self, dtype=None, copy=None):
            return self.data

    for cls in [MyArray, MyArray2]:
        x = np.arange(5)

        assert_(np.may_share_memory(cls(x[::2]), x[1::2]))
        assert_(not np.shares_memory(cls(x[::2]), x[1::2]))

        assert_(np.shares_memory(cls(x[1::3]), x[::2]))
        assert_(np.may_share_memory(cls(x[1::3]), x[::2]))

