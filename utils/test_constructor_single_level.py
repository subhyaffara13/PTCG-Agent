
def test_constructor_single_level():
    result = MultiIndex(
        levels=[["foo", "bar", "baz", "qux"]], codes=[[0, 1, 2, 3]], names=["first"]
    )
    assert isinstance(result, MultiIndex)
    expected = Index(["foo", "bar", "baz", "qux"], name="first")
    tm.assert_index_equal(result.levels[0], expected)
    assert result.names == ["first"]

