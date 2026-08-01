
def test_union_duplicates_different_names():
    # GH#62059
    mi1 = MultiIndex.from_tuples([(1, "a"), (2, "b")], names=["x", "y"])
    mi2 = MultiIndex.from_tuples([(2, "b"), (3, "c"), (2, "b")])

    result = mi1.union(mi2)
    expected = MultiIndex.from_tuples(
        [(1, "a"), (2, "b"), (2, "b"), (3, "c")], names=[None, None]
    )
    tm.assert_index_equal(result, expected)

