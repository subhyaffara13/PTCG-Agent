
def test_aggregate_datetime_objects():
    # https://github.com/pandas-dev/pandas/issues/36003
    # ensure we don't raise an error but keep object dtype for out-of-bounds
    # datetimes
    df = DataFrame(
        {
            "A": ["X", "Y"],
            "B": [
                datetime.datetime(2005, 1, 1, 10, 30, 23, 540000),
                datetime.datetime(3005, 1, 1, 10, 30, 23, 540000),
            ],
        }
    )
    result = df.groupby("A").B.max()
    expected = df.set_index("A")["B"]
    tm.assert_series_equal(result, expected)

