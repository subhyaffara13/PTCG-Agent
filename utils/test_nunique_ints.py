
def test_nunique_ints(index_or_series_or_array):
    # GH#36327
    values = index_or_series_or_array(np.random.default_rng(2).integers(0, 20, 30))
    result = algos.nunique_ints(values)
    expected = len(algos.unique(values))
    assert result == expected

