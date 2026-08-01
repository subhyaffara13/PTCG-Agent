
def test_to_numeric_scientific_notation():
    # GH 15898
    result = to_numeric("1.7e+308")
    expected = np.float64(1.7e308)
    assert result == expected

