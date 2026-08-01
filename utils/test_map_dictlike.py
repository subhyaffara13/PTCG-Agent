
def test_map_dictlike(idx, mapper):
    identity = mapper(idx.values, idx)

    # we don't infer to uint64 dtype for a dict
    if idx.dtype == np.uint64 and isinstance(identity, dict):
        expected = idx.astype("int64")
    else:
        expected = idx

    result = idx.map(identity)
    tm.assert_index_equal(result, expected)

    # empty mappable
    expected = Index([np.nan] * len(idx))
    result = idx.map(mapper(expected, idx))
    tm.assert_index_equal(result, expected)

