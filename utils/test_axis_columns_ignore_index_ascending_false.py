
def test_axis_columns_ignore_index_ascending_false():
    # GH 57293
    df = DataFrame(
        {
            "b": [1.0, 3.0, np.nan],
            "a": [1, 4, 3],
            1: ["a", "b", "c"],
            "e": [3, 1, 4],
            "d": [1, 2, 8],
        }
    ).set_index(["b", "a", 1])
    result = df.sort_index(axis="columns", ignore_index=True, ascending=False)
    expected = df.copy()
    expected.columns = RangeIndex(2)
    tm.assert_frame_equal(result, expected)

