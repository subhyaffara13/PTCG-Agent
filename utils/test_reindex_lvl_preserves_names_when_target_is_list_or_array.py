
def test_reindex_lvl_preserves_names_when_target_is_list_or_array():
    # GH7774
    idx = MultiIndex.from_product([[0, 1], ["a", "b"]], names=["foo", "bar"])
    assert idx.reindex([], level=0)[0].names == ["foo", "bar"]
    assert idx.reindex([], level=1)[0].names == ["foo", "bar"]

