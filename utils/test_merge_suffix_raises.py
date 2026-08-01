
def test_merge_suffix_raises(suffixes):
    a = DataFrame({"a": [1, 2, 3]})
    b = DataFrame({"b": [3, 4, 5]})

    with pytest.raises(TypeError, match="Passing 'suffixes' as a"):
        merge(a, b, left_index=True, right_index=True, suffixes=suffixes)

