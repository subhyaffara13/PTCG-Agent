
def test_accumulation(string_array, tile):
    """Accumulation is odd for StringDType but tests dtypes with references.
    """
    # Fill with mostly empty strings to not create absurdly big strings
    arr = np.zeros_like(string_array, shape=(100,))
    arr[:len(string_array)] = string_array
    arr[-len(string_array):] = string_array

    # Bloat size a bit (get above thresholds and test >1 ndim).
    arr = np.tile(string_array, tile)

    res = np.add.accumulate(arr, axis=0)
    res_obj = np.add.accumulate(arr.astype(object), axis=0)
    assert_array_equal(res, res_obj.astype(arr.dtype), strict=True)

    if arr.ndim > 1:
        res = np.add.accumulate(arr, axis=-1)
        res_obj = np.add.accumulate(arr.astype(object), axis=-1)

        assert_array_equal(res, res_obj.astype(arr.dtype), strict=True)

