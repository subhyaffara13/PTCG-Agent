
def test_duplicated_with_nan(val):
    # GH5873
    mi = MultiIndex.from_arrays([[101, val], [3.5, np.nan]])
    assert not mi.has_duplicates

    tm.assert_numpy_array_equal(mi.duplicated(), np.zeros(2, dtype="bool"))

