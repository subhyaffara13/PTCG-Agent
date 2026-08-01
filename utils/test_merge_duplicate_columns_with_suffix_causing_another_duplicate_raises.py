
def test_merge_duplicate_columns_with_suffix_causing_another_duplicate_raises():
    # GH#22818, Enforced in 2.0
    # This should raise warning because suffixes cause another collision
    left = DataFrame([[1, 1, 1, 1], [2, 2, 2, 2]], columns=["a", "b", "b", "b_x"])
    right = DataFrame({"a": [1, 3], "b": 2})
    with pytest.raises(MergeError, match="Passing 'suffixes' which cause duplicate"):
        merge(left, right, on="a")

