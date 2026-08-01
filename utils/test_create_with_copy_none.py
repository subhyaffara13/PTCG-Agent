
def test_create_with_copy_none(string_list):
    arr = np.array(string_list, dtype=StringDType())
    # create another stringdtype array with an arena that has a different
    # in-memory layout than the first array
    arr_rev = np.array(string_list[::-1], dtype=StringDType())

    # this should create a copy and the resulting array
    # shouldn't share an allocator or arena with arr_rev, despite
    # explicitly passing arr_rev.dtype
    arr_copy = np.array(arr, copy=None, dtype=arr_rev.dtype)
    np.testing.assert_array_equal(arr, arr_copy)
    assert arr_copy.base is None

    with pytest.raises(ValueError, match="Unable to avoid copy"):
        np.array(arr, copy=False, dtype=arr_rev.dtype)

    # because we're using arr's dtype instance, the view is safe
    arr_view = np.array(arr, copy=None, dtype=arr.dtype)
    np.testing.assert_array_equal(arr, arr)
    np.testing.assert_array_equal(arr_view[::-1], arr_rev)
    assert arr_view is arr

