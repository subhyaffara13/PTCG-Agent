
def test_array_equivalent_series(val):
    arr = np.array([1, 2])
    assert not array_equivalent(Series([arr, arr]), Series([arr, val]))

