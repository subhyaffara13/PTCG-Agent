
def test_unique_bad_unicode(index_or_series):
    # regression test for #34550
    uval = "\ud83d"  # smiley emoji

    obj = index_or_series([uval] * 2, dtype=object)
    result = obj.unique()

    if isinstance(obj, pd.Index):
        expected = pd.Index(["\ud83d"], dtype=object)
        tm.assert_index_equal(result, expected, exact=True)
    else:
        expected = np.array(["\ud83d"], dtype=object)
        tm.assert_numpy_array_equal(result, expected)

