
def test_series_mask_boolean(values, dtype, mask, indexer_class, frame):
    # In case len(values) < 3
    index = ["a", "b", "c"][: len(values)]
    mask = mask[: len(values)]

    obj = pd.Series(values, dtype=dtype, index=index)
    if frame:
        if len(values) == 0:
            # Otherwise obj is an empty DataFrame with shape (0, 1)
            obj = pd.DataFrame(dtype=dtype, index=index)
        else:
            obj = obj.to_frame()

    if indexer_class is pd.array:
        mask = pd.array(mask, dtype="boolean")
    elif indexer_class is pd.Series:
        mask = pd.Series(mask, index=obj.index, dtype="boolean")
    else:
        mask = indexer_class(mask)

    expected = obj[mask]

    result = obj[mask]
    tm.assert_equal(result, expected)

    if indexer_class is pd.Series:
        msg = "iLocation based boolean indexing cannot use an indexable as a mask"
        with pytest.raises(ValueError, match=msg):
            result = obj.iloc[mask]
    else:
        result = obj.iloc[mask]
        tm.assert_equal(result, expected)

    result = obj.loc[mask]
    tm.assert_equal(result, expected)

