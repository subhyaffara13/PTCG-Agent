
def test_droplevel_multiindex_one_level():
    # GH#37208
    index = MultiIndex.from_tuples([(2,)], names=("b",))
    result = index.droplevel([])
    expected = Index([2], name="b")
    tm.assert_index_equal(result, expected)

