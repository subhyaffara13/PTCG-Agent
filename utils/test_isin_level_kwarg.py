
def test_isin_level_kwarg():
    idx = MultiIndex.from_arrays([["qux", "baz", "foo", "bar"], np.arange(4)])

    vals_0 = ["foo", "bar", "quux"]
    vals_1 = [2, 3, 10]

    expected = np.array([False, False, True, True])
    tm.assert_numpy_array_equal(expected, idx.isin(vals_0, level=0))
    tm.assert_numpy_array_equal(expected, idx.isin(vals_0, level=-2))

    tm.assert_numpy_array_equal(expected, idx.isin(vals_1, level=1))
    tm.assert_numpy_array_equal(expected, idx.isin(vals_1, level=-1))

    msg = "Too many levels: Index has only 2 levels, not 6"
    with pytest.raises(IndexError, match=msg):
        idx.isin(vals_0, level=5)
    msg = "Too many levels: Index has only 2 levels, -5 is not a valid level number"
    with pytest.raises(IndexError, match=msg):
        idx.isin(vals_0, level=-5)

    with pytest.raises(KeyError, match=r"'Level 1\.0 not found'"):
        idx.isin(vals_0, level=1.0)
    with pytest.raises(KeyError, match=r"'Level -1\.0 not found'"):
        idx.isin(vals_1, level=-1.0)
    with pytest.raises(KeyError, match="'Level A not found'"):
        idx.isin(vals_1, level="A")

    idx.names = ["A", "B"]
    tm.assert_numpy_array_equal(expected, idx.isin(vals_0, level="A"))
    tm.assert_numpy_array_equal(expected, idx.isin(vals_1, level="B"))

    with pytest.raises(KeyError, match="'Level C not found'"):
        idx.isin(vals_1, level="C")

