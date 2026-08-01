
def test_reindex_empty_with_level(values):
    # GH41170
    ser = Series(
        range(len(values[0])), index=MultiIndex.from_arrays(values), dtype="object"
    )
    result = ser.reindex(np.array(["b"]), level=0)
    expected = Series(
        index=MultiIndex(levels=[["b"], values[1]], codes=[[], []]), dtype="object"
    )
    tm.assert_series_equal(result, expected)


def test_reindex_empty_with_level(values):
    # GH41170
    idx = MultiIndex.from_arrays(values)
    result, result_indexer = idx.reindex(np.array(["b"]), level=0)
    expected = MultiIndex(levels=[["b"], values[1]], codes=[[], []])
    expected_indexer = np.array([], dtype=result_indexer.dtype)
    tm.assert_index_equal(result, expected)
    tm.assert_numpy_array_equal(result_indexer, expected_indexer)

