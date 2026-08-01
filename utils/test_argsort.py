
def test_argsort(idx):
    result = idx.argsort()
    expected = idx.values.argsort()
    tm.assert_numpy_array_equal(result, expected)

