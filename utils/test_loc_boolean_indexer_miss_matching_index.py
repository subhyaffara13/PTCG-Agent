
def test_loc_boolean_indexer_miss_matching_index():
    # GH#46551
    ser = Series([1])
    indexer = Series([NA, False], dtype="boolean", index=[1, 2])
    with pytest.raises(IndexingError, match="Unalignable"):
        ser.loc[indexer]

