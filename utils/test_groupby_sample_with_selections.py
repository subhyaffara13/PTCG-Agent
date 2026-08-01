
def test_groupby_sample_with_selections():
    # GH 39928
    values = [1] * 10 + [2] * 10
    df = DataFrame({"a": values, "b": values, "c": values})

    result = df.groupby("a")[["b", "c"]].sample(n=None, frac=None)
    expected = DataFrame({"b": [1, 2], "c": [1, 2]}, index=result.index)
    tm.assert_frame_equal(result, expected)

