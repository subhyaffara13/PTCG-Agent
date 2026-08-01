
def test_dictlike_datetime_index_unsorted():
    # https://github.com/pandas-dev/pandas/pull/62843
    values = [datetime(2024, 1, 1), datetime(2024, 1, 2), datetime(2024, 1, 3)]
    df = DataFrame({"a": [1, 2], "b": [3, 4]}, index=[values[1], values[0]])
    result = df.apply(
        {"a": lambda x: x, "b": lambda x: x.shift(freq="D")}, by_row=False
    )
    expected = DataFrame(
        {
            "a": [1.0, 2.0, np.nan],
            "b": [4.0, np.nan, 3.0],
        },
        index=[values[1], values[0], values[2]],
    )
    tm.assert_frame_equal(result, expected)

