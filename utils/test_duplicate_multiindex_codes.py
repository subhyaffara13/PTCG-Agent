
def test_duplicate_multiindex_codes():
    # GH 17464
    # Make sure that a MultiIndex with duplicate levels throws a ValueError
    msg = r"Level values must be unique: \[[A', ]+\] on level 0"
    with pytest.raises(ValueError, match=msg):
        mi = MultiIndex([["A"] * 10, range(10)], [[0] * 10, range(10)])

    # And that using set_levels with duplicate levels fails
    mi = MultiIndex.from_arrays([["A", "A", "B", "B", "B"], [1, 2, 1, 2, 3]])
    msg = r"Level values must be unique: \[[AB', ]+\] on level 0"
    with pytest.raises(ValueError, match=msg):
        mi.set_levels([["A", "B", "A", "A", "B"], [2, 1, 3, -2, 5]])

