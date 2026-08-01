
def test_array_like_input(dtype):
    # Check that `_axis_nan_policy`-decorated functions work with custom
    # containers that are coercible to numeric arrays

    class ArrLike:
        def __init__(self, x, dtype):
            self._x = x
            self._dtype = dtype

        def __array__(self, dtype=None, copy=None):
            return np.asarray(x, dtype=self._dtype)

        def __iter__(self):
            # I don't know of a canonical way to determine whether an object should
            # be coerced to a NumPy array or not. Currently, `xp_promote` checks
            # whether they are iterable, and if so uses `_asarray` with whatever
            # `xp` is. So for this to get coerced, it needs to be iterable.
            return iter(self._x)

    x = [1]*2 + [3, 4, 5]
    res = stats.mode(ArrLike(x, dtype=dtype))
    assert res.mode == 1
    assert res.count == 2

