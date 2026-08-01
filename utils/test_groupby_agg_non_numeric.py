
def test_groupby_agg_non_numeric():
    df = DataFrame({"A": Categorical(["a", "a", "b"], categories=["a", "b", "c"])})
    expected = DataFrame({"A": [2, 1]}, index=np.array([1, 2]))

    result = df.groupby([1, 2, 1]).agg(Series.nunique)
    tm.assert_frame_equal(result, expected)

    result = df.groupby([1, 2, 1]).nunique()
    tm.assert_frame_equal(result, expected)

