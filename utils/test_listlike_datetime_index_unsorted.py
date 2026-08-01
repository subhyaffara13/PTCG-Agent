
def test_listlike_datetime_index_unsorted():
    # https://github.com/pandas-dev/pandas/pull/62843
    values = [datetime(2024, 1, 1), datetime(2024, 1, 2), datetime(2024, 1, 3)]
    df = DataFrame({"a": [1, 2]}, index=[values[1], values[0]])
    result = df.apply([lambda x: x, lambda x: x.shift(freq="D")], by_row=False)
    expected = DataFrame(
        [[1.0, 2.0], [2.0, np.nan], [np.nan, 1.0]],
        index=[values[1], values[0], values[2]],
        columns=MultiIndex([["a"], ["<lambda>"]], codes=[[0, 0], [0, 0]]),
    )
    tm.assert_frame_equal(result, expected)

