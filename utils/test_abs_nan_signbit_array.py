
def test_abs_nan_signbit_array():
    """#31421 abs(nan) array preserves positive sign bit correctly."""
    arr = np.array([np.nan, -np.nan])
    result = np.signbit(np.abs(arr))
    assert_array_equal(result, [False, False],
                      "abs of NaN array should have all positive signs")

