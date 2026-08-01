
def test_duplicated_index_getitem_positional_indexer(index_vals):
    # GH 11747; changed in 3.0 integers are treated as always-labels
    s = Series(range(5), index=list(index_vals))

    with pytest.raises(KeyError, match="^3$"):
        s[3]

