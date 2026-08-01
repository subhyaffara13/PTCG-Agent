
def test_add_timestamp_to_timedelta():
    # GH: 35897
    timestamp = Timestamp("2021-01-01")
    result = timestamp + timedelta_range("0s", "1s", periods=31)
    expected = DatetimeIndex(
        [
            timestamp
            + (
                pd.to_timedelta("0.033333s") * i
                + pd.to_timedelta("0.000001s") * divmod(i, 3)[0]
            )
            for i in range(31)
        ]
    )
    tm.assert_index_equal(result, expected)

