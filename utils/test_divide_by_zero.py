
def test_divide_by_zero(dtype, zero, negative, using_nan_is_na):
    # TODO pending NA/NaN discussion
    # https://github.com/pandas-dev/pandas/issues/32265/
    a = pd.array([0, 1, -1, None], dtype=dtype)
    result = a / zero
    exp_mask = np.array([False, False, False, True])
    if using_nan_is_na:
        exp_mask[[0, -1]] = True
    expected = FloatingArray(
        np.array([np.nan, np.inf, -np.inf, np.nan], dtype=dtype.numpy_dtype),
        exp_mask,
    )
    if negative:
        expected *= -1
    tm.assert_extension_array_equal(result, expected)


def test_divide_by_zero(zero, negative, using_nan_is_na):
    # https://github.com/pandas-dev/pandas/issues/27398, GH#22793
    a = pd.array([0, 1, -1, None], dtype="Int64")
    result = a / zero
    exp_mask = np.array([False, False, False, True])
    if using_nan_is_na:
        exp_mask[0] = True
    expected = FloatingArray(
        np.array([np.nan, np.inf, -np.inf, 1], dtype="float64"),
        exp_mask,
    )
    if negative:
        expected *= -1
    tm.assert_extension_array_equal(result, expected)

