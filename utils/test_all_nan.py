
def test_all_nan():
    ser = Series(["a", "b", "c"])
    result = to_numeric(ser, errors="coerce")

    expected = Series([np.nan, np.nan, np.nan])
    tm.assert_series_equal(result, expected)


def test_all_nan():
    x = np.array([[np.nan, np.nan], [np.nan, np.nan]])
    assert_array_almost_equal(plt.contour(x).levels,
                              [-1e-13, -7.5e-14, -5e-14, -2.4e-14, 0.0,
                                2.4e-14, 5e-14, 7.5e-14, 1e-13])

