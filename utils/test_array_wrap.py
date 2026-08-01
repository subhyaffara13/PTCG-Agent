
def test_array_wrap(subclass_self, subclass_arr):
    # NumPy should allow `__array_wrap__` to be called on arrays, it's logic
    # is designed in a way that:
    #
    # * Subclasses never return scalars by default (to preserve their
    #   information).  They can choose to if they wish.
    # * NumPy returns scalars, if `return_scalar` is passed as True to allow
    #   manual calls to `arr.__array_wrap__` to do the right thing.
    # * The type of the input should be ignored (it should be a base-class
    #   array, but I am not sure this is guaranteed).

    arr = np.arange(3).view(subclass_self)

    arr0d = np.array(3, dtype=np.int8).view(subclass_arr)
    # With third argument True, ndarray allows "decay" to scalar.
    # (I don't think NumPy would pass `None`, but it seems clear to support)
    if subclass_self is np.ndarray:
        assert type(arr.__array_wrap__(arr0d, None, True)) is np.int8
    else:
        assert type(arr.__array_wrap__(arr0d, None, True)) is type(arr)

    # Otherwise, result should be viewed as the subclass
    assert type(arr.__array_wrap__(arr0d)) is type(arr)
    assert type(arr.__array_wrap__(arr0d, None, None)) is type(arr)
    assert type(arr.__array_wrap__(arr0d, None, False)) is type(arr)

    # Non 0-D array can't be converted to scalar, so we ignore that
    arr1d = np.array([3], dtype=np.int8).view(subclass_arr)
    assert type(arr.__array_wrap__(arr1d, None, True)) is type(arr)


def test_array_wrap(scalar):
    # Test scalars array wrap as long as it exists.  NumPy itself should
    # probably not use it, so it may not be necessary to keep it around.

    arr0d = np.array(3, dtype=np.int8)
    # Third argument not passed, None, or True "decays" to scalar.
    # (I don't think NumPy would pass `None`, but it seems clear to support)
    assert type(scalar.__array_wrap__(arr0d)) is np.int8
    assert type(scalar.__array_wrap__(arr0d, None, None)) is np.int8
    assert type(scalar.__array_wrap__(arr0d, None, True)) is np.int8

    # Otherwise, result should be the input
    assert scalar.__array_wrap__(arr0d, None, False) is arr0d

    # An old bug.  A non 0-d array cannot be converted to scalar:
    arr1d = np.array([3], dtype=np.int8)
    assert scalar.__array_wrap__(arr1d) is arr1d
    assert scalar.__array_wrap__(arr1d, None, True) is arr1d

