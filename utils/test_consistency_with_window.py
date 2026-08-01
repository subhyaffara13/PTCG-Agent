
def test_consistency_with_window(test_frame):
    # consistent return values with window
    df = test_frame
    expected = Index([1, 2, 3], name="A")
    result = df.groupby("A").resample("2s").mean()
    assert result.index.nlevels == 2
    tm.assert_index_equal(result.index.levels[0], expected)

    result = df.groupby("A").rolling(20).mean()
    assert result.index.nlevels == 2
    tm.assert_index_equal(result.index.levels[0], expected)

