
def test_where_setitem_invalid():
    # GH 2702
    # make sure correct exceptions are raised on invalid list assignment

    msg = lambda x: (
        f"cannot set using a {x} indexer with a different length than the value"
    )
    # slice
    s = Series(list("abc"), dtype=object)

    with pytest.raises(ValueError, match=msg("slice")):
        s[0:3] = list(range(27))

    s[0:3] = list(range(3))
    expected = Series([0, 1, 2])
    tm.assert_series_equal(s.astype(np.int64), expected)

    # slice with step
    s = Series(list("abcdef"), dtype=object)

    with pytest.raises(ValueError, match=msg("slice")):
        s[0:4:2] = list(range(27))

    s = Series(list("abcdef"), dtype=object)
    s[0:4:2] = list(range(2))
    expected = Series([0, "b", 1, "d", "e", "f"])
    tm.assert_series_equal(s, expected)

    # neg slices
    s = Series(list("abcdef"), dtype=object)

    with pytest.raises(ValueError, match=msg("slice")):
        s[:-1] = list(range(27))

    s[-3:-1] = list(range(2))
    expected = Series(["a", "b", "c", 0, 1, "f"])
    tm.assert_series_equal(s, expected)

    # list
    s = Series(list("abc"), dtype=object)

    with pytest.raises(ValueError, match=msg("list-like")):
        s[[0, 1, 2]] = list(range(27))

    s = Series(list("abc"), dtype=object)

    with pytest.raises(ValueError, match=msg("list-like")):
        s[[0, 1, 2]] = list(range(2))

    # scalar
    s = Series(list("abc"), dtype=object)
    s[0] = list(range(10))
    expected = Series([list(range(10)), "b", "c"])
    tm.assert_series_equal(s, expected)

