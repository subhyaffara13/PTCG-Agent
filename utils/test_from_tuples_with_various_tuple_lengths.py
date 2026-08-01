
def test_from_tuples_with_various_tuple_lengths(keys, expected):
    # GH 60695
    idx = MultiIndex.from_tuples(keys)
    assert tuple(idx) == expected

