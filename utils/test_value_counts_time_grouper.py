
def test_value_counts_time_grouper(utc, unit):
    # GH#50486
    df = DataFrame(
        {
            "Timestamp": [
                1565083561,
                1565083561 + 86400,
                1565083561 + 86500,
                1565083561 + 86400 * 2,
                1565083561 + 86400 * 3,
                1565083561 + 86500 * 3,
                1565083561 + 86400 * 4,
            ],
            "Food": ["apple", "apple", "banana", "banana", "orange", "orange", "pear"],
        }
    ).drop([3])

    df["Datetime"] = to_datetime(df["Timestamp"], utc=utc, unit="s").dt.as_unit(unit)
    gb = df.groupby(Grouper(freq="1D", key="Datetime"))
    result = gb.value_counts()
    dates = to_datetime(
        ["2019-08-06", "2019-08-07", "2019-08-09", "2019-08-10"], utc=utc
    ).as_unit(unit)
    timestamps = df["Timestamp"].unique()
    index = MultiIndex(
        levels=[dates, timestamps, ["apple", "banana", "orange", "pear"]],
        codes=[[0, 1, 1, 2, 2, 3], range(6), [0, 0, 1, 2, 2, 3]],
        names=["Datetime", "Timestamp", "Food"],
    )
    expected = Series(1, index=index, name="count")
    tm.assert_series_equal(result, expected)

