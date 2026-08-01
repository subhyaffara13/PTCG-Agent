
def test_concat_multiindex_with_empty_rangeindex():
    # GH#41234
    mi = MultiIndex.from_tuples([("B", 1), ("C", 1)])
    df1 = DataFrame([[1, 2]], columns=mi)
    df2 = DataFrame(index=[1], columns=RangeIndex(0))

    result = concat([df1, df2])
    expected = DataFrame([[1, 2], [np.nan, np.nan]], columns=mi)
    tm.assert_frame_equal(result, expected)

