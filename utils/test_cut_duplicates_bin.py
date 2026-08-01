
def test_cut_duplicates_bin(kwargs, msg):
    # see gh-20947
    bins = [0, 2, 4, 6, 10, 10]
    values = Series(np.array([1, 3, 5, 7, 9]), index=["a", "b", "c", "d", "e"])

    if msg is not None:
        with pytest.raises(ValueError, match=msg):
            cut(values, bins, **kwargs)
    else:
        result = cut(values, bins, **kwargs)
        expected = cut(values, pd.unique(np.asarray(bins)))
        tm.assert_series_equal(result, expected)

