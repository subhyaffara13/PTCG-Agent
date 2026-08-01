
def test_get_level_lengths_mi_hidden():
    # GH 43464
    index = MultiIndex.from_arrays([[1, 1, 1, 2, 2, 2], ["a", "a", "b", "a", "a", "b"]])
    expected = {
        (0, 2): 1,
        (0, 3): 1,
        (0, 4): 1,
        (0, 5): 1,
        (1, 2): 1,
        (1, 3): 1,
        (1, 4): 1,
        (1, 5): 1,
    }
    result = _get_level_lengths(
        index,
        sparsify=False,
        max_index=100,
        hidden_elements=[0, 1, 0, 1],  # hidden element can repeat if duplicated index
    )
    tm.assert_dict_equal(result, expected)

