import copy

def test_array_called():
    class Wrapper:
        val = '0' * 100

        def __array__(self, dtype=None, copy=None):
            return np.array([self.val], dtype=dtype, copy=copy)

    wrapped = Wrapper()
    arr = np.array(wrapped, dtype=str)
    assert arr.dtype == 'U100'
    assert arr[0] == Wrapper.val

