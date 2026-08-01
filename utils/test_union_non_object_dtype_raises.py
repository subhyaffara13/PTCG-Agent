
def test_union_non_object_dtype_raises():
    # GH#32646 raise NotImplementedError instead of less-informative error
    mi = MultiIndex.from_product([["a", "b"], [1, 2]])

    idx = mi.levels[1]

    msg = "Can only union MultiIndex with MultiIndex or Index of tuples"
    with pytest.raises(NotImplementedError, match=msg):
        mi.union(idx)

