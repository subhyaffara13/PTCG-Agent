
def test_from_product_empty_one_level():
    result = MultiIndex.from_product([[]], names=["A"])
    expected = Index([], name="A")
    tm.assert_index_equal(result.levels[0], expected)
    assert result.names == ["A"]

