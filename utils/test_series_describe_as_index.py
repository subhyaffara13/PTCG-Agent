
def test_series_describe_as_index(as_index, keys):
    # GH#49256
    df = DataFrame(
        {
            "key1": ["one", "two", "two", "three", "two"],
            "key2": ["one", "two", "two", "three", "two"],
            "foo2": [1, 2, 4, 4, 6],
        }
    )
    gb = df.groupby(keys, as_index=as_index)["foo2"]
    result = gb.describe()
    expected = DataFrame(
        {
            "key1": ["one", "three", "two"],
            "count": [1.0, 1.0, 3.0],
            "mean": [1.0, 4.0, 4.0],
            "std": [np.nan, np.nan, 2.0],
            "min": [1.0, 4.0, 2.0],
            "25%": [1.0, 4.0, 3.0],
            "50%": [1.0, 4.0, 4.0],
            "75%": [1.0, 4.0, 5.0],
            "max": [1.0, 4.0, 6.0],
        }
    )
    if len(keys) == 2:
        expected.insert(1, "key2", expected["key1"])
    if as_index:
        expected = expected.set_index(keys)
    tm.assert_frame_equal(result, expected)

