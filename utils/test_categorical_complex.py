
def test_categorical_complex():
    result = Categorical([1, 2 + 2j])
    expected = Categorical([1.0 + 0.0j, 2.0 + 2.0j])
    tm.assert_categorical_equal(result, expected)
    result = Categorical([1, 2, 2 + 2j])
    expected = Categorical([1.0 + 0.0j, 2.0 + 0.0j, 2.0 + 2.0j])
    tm.assert_categorical_equal(result, expected)

