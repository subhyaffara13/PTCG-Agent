
def test_reindex_preserves_names_when_target_is_list_or_ndarray(idx):
    # GH6552
    idx = idx.copy()
    target = idx.copy()
    idx.names = target.names = [None, None]

    other_dtype = MultiIndex.from_product([[1, 2], [3, 4]])

    # list & ndarray cases
    assert idx.reindex([])[0].names == [None, None]
    assert idx.reindex(np.array([]))[0].names == [None, None]
    assert idx.reindex(target.tolist())[0].names == [None, None]
    assert idx.reindex(target.values)[0].names == [None, None]
    assert idx.reindex(other_dtype.tolist())[0].names == [None, None]
    assert idx.reindex(other_dtype.values)[0].names == [None, None]

    idx.names = ["foo", "bar"]
    assert idx.reindex([])[0].names == ["foo", "bar"]
    assert idx.reindex(np.array([]))[0].names == ["foo", "bar"]
    assert idx.reindex(target.tolist())[0].names == ["foo", "bar"]
    assert idx.reindex(target.values)[0].names == ["foo", "bar"]
    assert idx.reindex(other_dtype.tolist())[0].names == ["foo", "bar"]
    assert idx.reindex(other_dtype.values)[0].names == ["foo", "bar"]

