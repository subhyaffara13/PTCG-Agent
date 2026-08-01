
def test_assert_index_equal_categorical_incomparable_categories():
    # GH#61935
    left = Index([1, 2, 3], name="a", dtype="category")
    right = Index([1, 2, 6], name="a", dtype="category")
    with pytest.raises(AssertionError, match="types are not comparable"):
        tm.assert_index_equal(left, right, check_categorical=True, exact=False)

