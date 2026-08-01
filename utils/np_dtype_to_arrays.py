
def np_dtype_to_arrays(any_real_numpy_dtype):
    """
    Fixture returning actual and expected dtype, pandas and numpy arrays and
    mask from a given numpy dtype
    """
    np_dtype = np.dtype(any_real_numpy_dtype)
    pa_type = pa.from_numpy_dtype(np_dtype)

    # None ensures the creation of a bitmask buffer.
    pa_array = pa.array([0, 1, 2, None], type=pa_type)
    # Since masked Arrow buffer slots are not required to contain a specific
    # value, assert only the first three values of the created np.array
    np_expected = np.array([0, 1, 2], dtype=np_dtype)
    mask_expected = np.array([True, True, True, False])
    return np_dtype, pa_array, np_expected, mask_expected

