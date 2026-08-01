
def test_hasnans_isnans(idx):
    # GH 11343, added tests for hasnans / isnans
    index = idx.copy()

    # cases in indices doesn't include NaN
    expected = np.array([False] * len(index), dtype=bool)
    tm.assert_numpy_array_equal(index._isnan, expected)
    assert index.hasnans is False

    index = idx.copy()
    values = index.values
    values[1] = np.nan

    index = type(idx)(values)

    expected = np.array([False] * len(index), dtype=bool)
    expected[1] = True
    tm.assert_numpy_array_equal(index._isnan, expected)
    assert index.hasnans is True

