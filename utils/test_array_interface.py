
def test_array_interface(idx):
    # https://github.com/pandas-dev/pandas/pull/60046
    result = np.asarray(idx)
    expected = np.empty((6,), dtype=object)
    expected[:] = [
        ("foo", "one"),
        ("foo", "two"),
        ("bar", "one"),
        ("baz", "two"),
        ("qux", "one"),
        ("qux", "two"),
    ]
    tm.assert_numpy_array_equal(result, expected)

    # it always gives a copy by default, but the values are cached, so results
    # are still sharing memory
    result_copy1 = np.asarray(idx)
    result_copy2 = np.asarray(idx)
    assert np.may_share_memory(result_copy1, result_copy2)

    # with explicit copy=True, then it is an actual copy
    result_copy1 = np.array(idx, copy=True)
    result_copy2 = np.array(idx, copy=True)
    assert not np.may_share_memory(result_copy1, result_copy2)

    if not np_version_gt2:
        # copy=False semantics are only supported in NumPy>=2.
        return

    # for MultiIndex, copy=False is never allowed
    with pytest.raises(ValueError, match="Unable to avoid copy while creating"):
        np.array(idx, copy=False)


def test_array_interface(arr_data, arr):
    # https://github.com/pandas-dev/pandas/pull/60046
    result = np.asarray(arr)
    tm.assert_numpy_array_equal(result, arr_data)

    # it always gives a copy by default
    result_copy1 = np.asarray(arr)
    result_copy2 = np.asarray(arr)
    assert not np.may_share_memory(result_copy1, result_copy2)

    # or with explicit copy=True
    result_copy1 = np.array(arr, copy=True)
    result_copy2 = np.array(arr, copy=True)
    assert not np.may_share_memory(result_copy1, result_copy2)

    if not np_version_gt2:
        # copy=False semantics are only supported in NumPy>=2.
        return

    # for sparse arrays, copy=False is never allowed
    with pytest.raises(ValueError, match="Unable to avoid copy while creating"):
        np.array(arr, copy=False)

    # except when there are actually no sparse filled values
    arr2 = SparseArray(np.array([1, 2, 3]))
    result_nocopy1 = np.array(arr2, copy=False)
    result_nocopy2 = np.array(arr2, copy=False)
    assert np.may_share_memory(result_nocopy1, result_nocopy2)

