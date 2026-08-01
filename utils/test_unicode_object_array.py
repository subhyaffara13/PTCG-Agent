
def test_unicode_object_array():
    expected = "array(['é'], dtype=object)"
    x = np.array(['\xe9'], dtype=object)
    assert_equal(repr(x), expected)

