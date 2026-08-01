
def test_groupby_as_index_cython(df):
    data = df

    # single-key
    grouped = data.groupby("A", as_index=False)
    result = grouped.mean(numeric_only=True)
    expected = data.groupby(["A"]).mean(numeric_only=True)
    expected.insert(0, "A", expected.index)
    expected.index = RangeIndex(len(expected))
    tm.assert_frame_equal(result, expected)

    # multi-key
    grouped = data.groupby(["A", "B"], as_index=False)
    result = grouped.mean()
    expected = data.groupby(["A", "B"]).mean()

    arrays = list(zip(*expected.index.values, strict=True))
    expected.insert(0, "A", arrays[0])
    expected.insert(1, "B", arrays[1])
    expected.index = RangeIndex(len(expected))
    tm.assert_frame_equal(result, expected)

