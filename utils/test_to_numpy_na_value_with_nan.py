
def test_to_numpy_na_value_with_nan(using_nan_is_na):
    # array with both NaN and NA -> only fill NA with `na_value`
    mask = np.array([False, False, True])
    if using_nan_is_na:
        mask[1] = True
    arr = FloatingArray(np.array([0.0, np.nan, 0.0]), mask)
    result = arr.to_numpy(dtype="float64", na_value=-1)
    if using_nan_is_na:
        # the NaN passed to the constructor is considered as NA
        expected = np.array([0.0, -1.0, -1.0], dtype="float64")
    else:
        expected = np.array([0.0, np.nan, -1.0], dtype="float64")
    tm.assert_numpy_array_equal(result, expected)

