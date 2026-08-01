
def test_map_type():
    # GH 46719
    s = Series([3, "string", float], index=["a", "b", "c"])
    result = s.map(type)
    expected = Series([int, str, type], index=["a", "b", "c"])
    tm.assert_series_equal(result, expected)


def test_map_type():
    # GH 46719
    df = DataFrame(
        {"col1": [3, "string", float], "col2": [0.25, datetime(2020, 1, 1), np.nan]},
        index=["a", "b", "c"],
    )

    result = df.map(type)
    expected = DataFrame(
        {"col1": [int, str, type], "col2": [float, datetime, float]},
        index=["a", "b", "c"],
    )
    tm.assert_frame_equal(result, expected)

