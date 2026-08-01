
def test_assert_numpy_array_equal_bad_type():
    expected = "Expected type"

    with pytest.raises(AssertionError, match=expected):
        tm.assert_numpy_array_equal(1, 2)

