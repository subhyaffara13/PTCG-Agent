
def test_mixed_type():
    s = pd.Series(
        [[0, 1, 2], np.nan, None, np.array([]), pd.Series(["a", "b"])], name="foo"
    )
    result = s.explode()
    expected = pd.Series(
        [0, 1, 2, np.nan, None, np.nan, "a", "b"],
        index=[0, 0, 0, 1, 2, 3, 4, 4],
        dtype=object,
        name="foo",
    )
    tm.assert_series_equal(result, expected)

