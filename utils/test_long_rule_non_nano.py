
def test_long_rule_non_nano():
    # https://github.com/pandas-dev/pandas/issues/51024
    idx = date_range("0300-01-01", "2000-01-01", unit="s", freq="100YE")
    ser = Series([1, 4, 2, 8, 5, 7, 1, 4, 2, 8, 5, 7, 1, 4, 2, 8, 5], index=idx)
    result = ser.resample("200YE").mean()
    expected_idx = DatetimeIndex(
        np.array(
            [
                "0300-12-31",
                "0500-12-31",
                "0700-12-31",
                "0900-12-31",
                "1100-12-31",
                "1300-12-31",
                "1500-12-31",
                "1700-12-31",
                "1900-12-31",
            ]
        ).astype("datetime64[s]"),
        freq="200YE-DEC",
    )
    expected = Series([1.0, 3.0, 6.5, 4.0, 3.0, 6.5, 4.0, 3.0, 6.5], index=expected_idx)
    tm.assert_series_equal(result, expected)

