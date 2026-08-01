
def test_series_getitem_duplicates_multiindex(level0_value):
    # GH 5725 the 'A' happens to be a valid Timestamp so the doesn't raise
    # the appropriate error, only in PY3 of course!

    index = MultiIndex(
        levels=[[level0_value, "B", "C"], [0, 26, 27, 37, 57, 67, 75, 82]],
        codes=[[0, 0, 0, 1, 2, 2, 2, 2, 2, 2], [1, 3, 4, 6, 0, 2, 2, 3, 5, 7]],
        names=["tag", "day"],
    )
    arr = np.random.default_rng(2).standard_normal((len(index), 1))
    df = DataFrame(arr, index=index, columns=["val"])

    # confirm indexing on missing value raises KeyError
    if level0_value != "A":
        with pytest.raises(KeyError, match=r"^'A'$"):
            df.val["A"]

    with pytest.raises(KeyError, match=r"^'X'$"):
        df.val["X"]

    result = df.val[level0_value]
    expected = Series(
        arr.ravel()[0:3], name="val", index=Index([26, 37, 57], name="day")
    )
    tm.assert_series_equal(result, expected)

