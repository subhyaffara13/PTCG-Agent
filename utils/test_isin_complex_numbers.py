
def test_isin_complex_numbers():
    # GH 17927
    array = [0, 1j, 1j, 1, 1 + 1j, 1 + 2j, 1 + 1j]
    result = Series(array).isin([1j, 1 + 1j, 1 + 2j])
    expected = Series([False, True, True, False, True, True, True], dtype=bool)
    tm.assert_series_equal(result, expected)

