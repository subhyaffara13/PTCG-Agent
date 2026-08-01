
def test_rolling_std_small_values():
    # GH 37051
    s = Series(
        [
            0.00000054,
            0.00000053,
            0.00000054,
        ]
    )
    result = s.rolling(2).std()
    expected = Series([np.nan, 7.071068e-9, 7.071068e-9])
    tm.assert_series_equal(result, expected, atol=1.0e-15, rtol=1.0e-15)

