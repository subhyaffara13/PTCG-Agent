
def test_apply_frame_to_series(df):
    grouped = df.groupby(["A", "B"])
    result = grouped.apply(len)
    expected = grouped.count()["C"]
    tm.assert_index_equal(result.index, expected.index)
    tm.assert_numpy_array_equal(result.values, expected.values)

